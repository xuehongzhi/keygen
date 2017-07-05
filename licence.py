import rsa
import os
from datetime import datetime
from base64 import b32encode, b32decode
from distutils.version import StrictVersion

#BASE32(CONCAT(PRIVATE_KEY_ENCRYPTED(HASH(DATA)), DATA))


class LicDataError(Exception):
    def __init__(self, desc):
        self.desc = desc

    def __str__(self):
        return repr(self.desc)


class LicDateInvalid(Exception):
    def __init__(self, desc):
        self.desc = desc

    def __str__(self):
        return repr(self.desc)


class LicItemError(Exception):
    def __init__(self, desc):
        self.desc = desc

    def __str__(self):
        return repr(self.desc)


def new_keys(product, nbits=256):
    fpath = '{}_private'.format(product)
    keys = None
    try:
        with open(fpath, 'rb') as fp:
            pri_key = rsa.key.PrivateKey.load_pkcs1(fp.read())
            pub_key = rsa.key.PublicKey(n=pri_key.n, e=65537)
            keys = pub_key, pri_key
    except Exception as e:
        print(e)
        with open(fpath, 'wb') as fp:
            keys = rsa.newkeys(nbits)
            fp.write(keys[1].save_pkcs1())
    return keys


def get_lic_info(licfile, pub_key):
    try:
        with open(licfile, 'rb') as fp:
            encdata = b32decode(fp.read())
            message, sig = encdata[256:], encdata[:256]
            print('reg info is %s' %(message.decode(), ))
            if rsa.verify(message, sig, pub_key):
                return dict([msg.split(':') for msg in message.decode().split(';')])
    except rsa.VerificationError:
        raise LicDataError('invalid key')
    except FileNotFoundError:
        raise LicDataError('no key data exist')


def get_maccode():
    import netifaces as nf
    try:
        return nf.gateways()['default'][nf.AF_INET][1].strip('{}')
    except BaseException:
        return None


class LicItemMatcher:
    def __init__(self, name, locval):
        self.name = name
        self.locval = locval

    def match(self, licval, locval):
        if licval != locval:
            raise LicItemError('%s is mismatched' % (self.name, ))

    def test(self, lic):
        licval = lic.pop(self.name)
        if not licval:
            raise LicItemError('%s is missing' % (self.name, ))
        self.match(licval, self.locval)


class DateMatcher(LicItemMatcher):
    def match(self, licval, locval):
        edate = licval
        locval = locval.timestamp()
        if locval > float(edate):
            raise LicDateInvalid('licence is expired')



class VersionMatcher(LicItemMatcher):
    def match(self, licval, locval):
        if StrictVersion(locval) != StrictVersion(licval):
            raise LicItemError('version is mismatched')

def key_gen(maccode, product, version='1.0', edate=None, keyfile=None, **kwargs):
    try:
        pub_key, pri_key = new_keys(product, nbits=2048)

        if not edate:
            sdate = datetime.now()
            edate = sdate.replace(year=sdate.year+1)

        edate = datetime.utcfromtimestamp(edate.timestamp())
        #print(edate)
        message = 'maccode:{};product:{};version:{};expire-date:{};{}'.format(
            maccode, product, version,
            edate.timestamp(),
            ';'.join(['{}:{}'.format(k, v) for k, v in kwargs.items()])).strip(';').encode()
        print(message)
        sig = rsa.sign(message, pri_key, 'SHA-256')
        encdata = b32encode(sig+message)
        kf = keyfile if keyfile else '%s.lic' % (product,)
        with open(kf, 'wb') as fp:
            fp.write(encdata)
        return encdata, pub_key
    except BaseException:
        raise


def check_lic(licfile, pub_key):
    # machine code mismatched
    try:
        locrec = {
            'maccode': LicItemMatcher(
                'maccode', get_maccode()), 'product': LicItemMatcher(
                'product', 'otsweb'), 'expire-date': DateMatcher(
                    'expire-date', datetime.utcfromtimestamp(
                        datetime.now().timestamp())),
                'version': VersionMatcher('version', '1.0')}
        licrec = get_lic_info(licfile, pub_key)
        for k, v in locrec.items():
            v.test(licrec)
    except:
        raise


if __name__ == '__main__':
    maccode = get_maccode()
    print('machine code is %s' % (maccode,))
    product = 'otsweb'
    #enc, pub_key = key_gen(maccode, product)
    #print('key is %s' % (enc, ))
    _, pub_key = new_keys(product)
    try:
        licinfo = get_lic_info('{}.lic'.format(product), pub_key)
        print(licinfo)
        check_lic('{}.lic'.format(product), pub_key)
        print('licence is valid')
    except Exception as e:
        print(e)
