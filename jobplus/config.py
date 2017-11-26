class BaseConfig(object):
    """配置基类"""
    SECRET_KEY = 'makesure to set a very secret key'
    INDEX_PER_PAGE = 9
    ADMIN_PRE_PAGE = 15


class DevelopmentConfig(BaseConfig):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:zmxhdu@localhost:3306/recruiment?charset=utf8'


class ProductionConfig(BaseConfig):
    """生产环境配置"""
    pass


class TestingConfig(BaseConfig):
    """测试环境配置"""
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}