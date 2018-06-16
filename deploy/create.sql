/*创建新表*/


/*Table structure for table `user` */
/*用户表*/
CREATE TABLE user (
      id int(11) NOT NULL AUTO_INCREMENT,

      username	varchar(255) NOT NULL UNIQUE,  /*用户名*/
      passwd varchar(255) NOT NULL, /*密码*/
      role	int(11) NOT NULL DEFAULT 0, /*用户角色 1：普通用户； 2： 管理员*/
      forbidden int(11) NOT NULL DEFAULT 0, /*是否被封禁 0：未被封禁； 1： 被封禁*/
      active	int(11) NOT NULL, /*登录时间*/
      token_time	int(11) NOT NULL, /* 生成token的时间*/
      created_at	int(11) NOT NULL, /*用户创建时间戳*/
      PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;


/*初始化管理员   用户名: admin   密码: 123456*/
INSERT INTO user(username,passwd,role) values('admin', 'ba3253876aed6bc22d4a6ff53d8406c6ad864195ed144ab5c87621b6c233b548baeae6956df346ec8c17f5ea10f35ee3cbc514797ed7ddd3145464e2a0bab413', 2);