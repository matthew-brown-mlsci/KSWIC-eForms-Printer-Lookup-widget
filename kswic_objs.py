"""

KSWIC eForms Printer Lookup objects

"""

class domain_obj(object):
    def __init__(self,
                domain,
                base_dn,
                ldap_servers
                ):
        self.domain = domain
        self.base_dn = base_dn
        self.ldap_servers = ldap_servers

    def serialize(self):
        return {
            'domain': self.domain,
            'base_dn': self.base_dn,
            'ldap_servers': [e for e in self.ldap_servers]
        }
