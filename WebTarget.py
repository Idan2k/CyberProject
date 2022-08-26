from Target import Target


class WebTarget(Target):
    def __init__(self, ip, homepage):
        Target.__init__(self, ip)
        self.__homepage = homepage
        self.__user_cookies = []
        self.__site_cookies = []
        self.__sqli_payloads = dict({})
        # key - vulnerURL, value - "{METHOD TYPE/COOKIE},{VULNER_PARAMETER/COOKIE},[{SQLi_TYPE},{TITLE}, {SQLi_PAYLOAD}](*3)"
        # vulner_url = ''
        # method_type = ''
        # vulner_param = ''
        # sqli_type = ''
        # sqli_payload = ''

    def __repr__(self):
        super().__repr__()
        return f'WebTarget({repr(Target(self))}, "{self.__homepage}", "{self.__user_cookies}"' \
               f'"{self.__sqli_payloads}'
    # PROPERTIES
    # --------------------------------------------
    # USER COOKIES PROPERTY
    @property
    # Getter method
    def user_cookies(self):
        return self.__user_cookies

    # Setter method
    @user_cookies.setter
    def user_cookies(self, val):
        self.__user_cookies = val

    # --------------------------------------------

    # SITE COOKIES PROPERTY
    @property
    # Getter method
    def site_cookies(self):
        return self.__site_cookies

    # Setter method
    @site_cookies.setter
    def site_cookies(self, val):
        self.__site_cookies = val

    # --------------------------------------------

    # HOMEPAGE PROPERTY
    @property
    # Getter method
    def homepage(self):
        return self.__homepage

    # Setter method
    @homepage.setter
    def homepage(self, val):
        self.__homepage = val

# --------------------------------------------

    # SQLi PAYLOADS PROPERTY
    @property
    # Getter method
    def sqli_payloads(self):
        return self.__SQLi_payloads

    # Setter method
    @sqli_payloads.setter
    def sqli_payloads(self, val):
        self.__SQLi_payloads = val

