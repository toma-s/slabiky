from config_data import ConfigData

conf = ConfigData('conf/conf_be_cyr.json', 'utf-8')
print(conf.lang_name)
print(conf.lang_wr_sys)
print(conf.uppercase)
print(conf.lowercase)