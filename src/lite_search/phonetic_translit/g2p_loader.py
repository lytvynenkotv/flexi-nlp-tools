import ssl
import nltk
import certifi
from g2p_en import G2p


# ssl._create_default_https_context = ssl.create_default_context
# ssl._create_default_https_context().load_verify_locations(certifi.where())
# nltk.download('averaged_perceptron_tagger')


_G2P_MODEL: G2p = None


def get_g2p_model() -> G2p:
    global _G2P_MODEL
    if _G2P_MODEL is None:
        _G2P_MODEL = G2p()

    return _G2P_MODEL
