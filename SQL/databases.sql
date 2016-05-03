# ************************************************************
# Sequel Pro SQL dump
# Version 4135
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.42)
# Database: python
# Generation Time: 2016-05-03 10:37:25 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table project
# ------------------------------------------------------------

DROP TABLE IF EXISTS `project`;

CREATE TABLE `project` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL DEFAULT '' COMMENT '项目名',
  `tname` varchar(255) NOT NULL DEFAULT '' COMMENT '表名',
  `start_url` varchar(255) NOT NULL DEFAULT '' COMMENT '起始URL地址',
  `craw_num` int(11) NOT NULL COMMENT '爬行页上限',
  `url_regex` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='项目表';

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;

INSERT INTO `project` (`id`, `title`, `tname`, `start_url`, `craw_num`, `url_regex`)
VALUES
    (1,'测试项目','baidubaike','http://baike.baidu.com/subview/99/5828265.htm',5,'/view/\\d+\\.htm');

/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table project_field
# ------------------------------------------------------------

DROP TABLE IF EXISTS `project_field`;

CREATE TABLE `project_field` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL COMMENT '项目ID',
  `field` varchar(255) NOT NULL DEFAULT '' COMMENT '数据库表字段名',
  `field_type` varchar(255) NOT NULL DEFAULT '' COMMENT '字段类型',
  `soup_rules` varchar(255) NOT NULL DEFAULT '' COMMENT 'SOUP取公式',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='项目详细攫取字段表';

LOCK TABLES `project_field` WRITE;
/*!40000 ALTER TABLE `project_field` DISABLE KEYS */;

INSERT INTO `project_field` (`id`, `pid`, `field`, `field_type`, `soup_rules`)
VALUES
    (1,1,'biaoti','varchar','soup.find( \'dd\', class_=\"lemmaWgt-lemmaTitle-title\").find(\"h1\")'),
    (2,1,'jianjie','text','soup.find(\'div\', class_=\"lemma-summary\")'),
    (4,2,'title','varchar','');

/*!40000 ALTER TABLE `project_field` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
