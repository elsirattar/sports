DROP TABLE IF EXISTS `activity`;
CREATE TABLE `activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `coach` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `trainer` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `category` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `start` time NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `activity` VALUES("1", "ahmed", "ali", "كاراتيه", "10:04:11", "2023-06-27");
INSERT INTO `activity` VALUES("2", "عمر ", "ahmed", "karate", "8:10:00", "2023-06-27");
INSERT INTO `activity` VALUES("3", "عمر ", "ahmed", "karate", "0:00:00", "2023-06-27");
INSERT INTO `activity` VALUES("4", "عمر ", "majed", "جمباز", "0:00:00", "2023-06-27");
INSERT INTO `activity` VALUES("5", "محمد سليم ", "ahmed", "karate", "8:11:00", "2023-06-27");
INSERT INTO `activity` VALUES("6", "محمد سليم ", "majed", "جمباز", "8:11:00", "2023-06-27");
INSERT INTO `activity` VALUES("7", "عمر ", "ahmed", "كاراتية", "14:47:00", "2023-07-25");
INSERT INTO `activity` VALUES("8", "عمر ", "majed", "جودو ", "14:47:00", "2023-07-25");
INSERT INTO `activity` VALUES("9", "عمر ", "ali", "كاراتية", "14:47:00", "2023-07-25");
INSERT INTO `activity` VALUES("10", "عمر ", "maher", "جودو ", "14:47:00", "2023-07-25");
INSERT INTO `activity` VALUES("11", "عمر ", "majed", "جودو ", "14:33:00", "2023-07-25");
INSERT INTO `activity` VALUES("12", "tarek", "majed", "جودو ", "14:33:00", "2023-07-25");


DROP TABLE IF EXISTS `app_data`;
CREATE TABLE `app_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `confirm` int(1) NOT NULL DEFAULT '1',
  `sending` int(1) NOT NULL DEFAULT '0',
  `db_path` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL DEFAULT '0',
  `mail` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `app_data` VALUES("1", "0", "0", "C:\Users\ahmedalattar\Desktop\programming", "medoselim55@gmail.com");


DROP TABLE IF EXISTS `clients`;
CREATE TABLE `clients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `phone` varchar(11) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `clients` VALUES("1", "adam", "01020374108");
INSERT INTO `clients` VALUES("2", "majed", "1245789631");
INSERT INTO `clients` VALUES("3", "ali", "01254856");
INSERT INTO `clients` VALUES("4", "maher", "1236547896");
INSERT INTO `clients` VALUES("5", "wael", "1254879630");
INSERT INTO `clients` VALUES("6", "samy", "2154879630");
INSERT INTO `clients` VALUES("7", "emad", "1245879630");
INSERT INTO `clients` VALUES("8", "مجدى ", "124578963");


DROP TABLE IF EXISTS `coach`;
CREATE TABLE `coach` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `phone` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `category` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `coach` VALUES("1", "عمر ", "01020398452", "كاراتية");
INSERT INTO `coach` VALUES("2", "احمد العطار", "01245789630", "كاراتية");
INSERT INTO `coach` VALUES("3", "tarek", "01485236970", "كاراتية");
INSERT INTO `coach` VALUES("4", "محمد سليم", "0121201201", "كاراتية");
INSERT INTO `coach` VALUES("5", "محمد سليم ", "01254789630", "جودو ");


DROP TABLE IF EXISTS `daily_sales`;
CREATE TABLE `daily_sales` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `phone` varchar(11) COLLATE utf8_general_mysql500_ci NOT NULL,
  `groups` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `package` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `count` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `finish` date NOT NULL,
  `invoice` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `daily_sales` VALUES("1", "ahmed", "", "karate", "شهر", "3", "25", "2023-06-25", "2023-06-30", "INV-00001");
INSERT INTO `daily_sales` VALUES("2", "majed", "1245789631", "swimming", "تمرين 2", "8", "150", "2023-06-25", "2023-06-20", "INV-00002");
INSERT INTO `daily_sales` VALUES("3", "majed", "1245789631", "جمباز", "سنوية", "150", "300", "2023-06-27", "2023-06-06", "INV-00003");
INSERT INTO `daily_sales` VALUES("4", "majed", "1245789631", "جمباز", "شهر", "13", "140", "2023-06-27", "2023-06-30", "INV-00003");
INSERT INTO `daily_sales` VALUES("5", "majed", "1245789631", "كاراتية", "شهر", "14", "150", "2023-06-27", "2023-06-30", "INV-00004");
INSERT INTO `daily_sales` VALUES("6", "majed", "1245789631", "جودو ", "تمرين ", "1", "10", "2023-06-27", "2023-06-30", "INV-00005");
INSERT INTO `daily_sales` VALUES("7", "majed", "1245789631", "كاراتية", "شهر", "14", "150", "2023-06-27", "2023-06-30", "INV-00006");
INSERT INTO `daily_sales` VALUES("8", "majed", "1245789631", "كاراتية", "شهر", "14", "150", "2023-06-27", "2023-06-30", "INV-00007");
INSERT INTO `daily_sales` VALUES("9", "ahmed", "120120120", "كاراتية", "شهر", "14", "150", "2023-06-27", "2023-06-30", "INV-00008");
INSERT INTO `daily_sales` VALUES("10", "majed", "1245789631", "جودو ", "تمرين ", "1", "10", "2023-06-27", "2023-06-30", "INV-00009");
INSERT INTO `daily_sales` VALUES("11", "majed", "1245789631", "كاراتية", "شهر", "14", "150", "2023-06-27", "2023-06-30", "INV-00010");
INSERT INTO `daily_sales` VALUES("12", "ahmed", "120120120", "كاراتية", "شهر", "14", "150", "2023-06-27", "2023-06-30", "INV-00011");
INSERT INTO `daily_sales` VALUES("13", "ahmed", "120120120", "جودو ", "تمرين ", "1", "10", "2023-06-27", "2023-06-30", "INV-00012");
INSERT INTO `daily_sales` VALUES("14", "majed", "1245789631", "جودو ", "تمرين ", "1", "10", "2023-07-11", "2023-07-31", "INV-00013");
INSERT INTO `daily_sales` VALUES("15", "ali", "1254879660", "كاراتية", "بسم الله الرحمن الرحيم", "4", "200", "2023-07-25", "2023-07-31", "INV-00014");
INSERT INTO `daily_sales` VALUES("16", "maher", "1236547896", "جودو ", "تمرين ", "1", "10", "2023-07-25", "2023-07-31", "INV-00015");
INSERT INTO `daily_sales` VALUES("17", "ahmed", "120120120", "كاراتية", "شهر", "14", "150", "2023-07-25", "2023-07-31", "INV-00016");
INSERT INTO `daily_sales` VALUES("18", "maher", "1236547896", "كاراتية", "1", "4", "200", "2023-07-25", "2023-07-31", "INV-00017");
INSERT INTO `daily_sales` VALUES("19", "majed", "1245789631", "كاراتية", "شهر", "14", "150", "2023-07-25", "2023-07-31", "INV-00018");
INSERT INTO `daily_sales` VALUES("20", "waleed", "1254879630", "جودو ", "تمرين ", "1", "10", "2023-07-25", "2023-07-31", "INV-00019");
INSERT INTO `daily_sales` VALUES("21", "samy", "2154879630", "كاراتية", "بسم الله الرحمن الرحيم", "4", "200", "2023-07-25", "2023-07-31", "INV-00020");
INSERT INTO `daily_sales` VALUES("22", "emad", "1245879630", "كاراتية", "بسم الله الرحمن الرحيم", "4", "200", "2023-07-25", "2023-07-31", "INV-00021");
INSERT INTO `daily_sales` VALUES("23", "emad", "1245879630", "كاراتية", "بسم الله الرحمن الرحيم", "4", "200", "2023-07-25", "2023-07-31", "INV-00022");
INSERT INTO `daily_sales` VALUES("24", "adam", "01020374108", "كاراتية", "شهر", "14", "150", "2023-07-30", "2023-07-31", "INV-00023");


DROP TABLE IF EXISTS `expense`;
CREATE TABLE `expense` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `price` int(11) NOT NULL,
  `status` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `expense` VALUES("1", "راتب", "1500", "شهر يونيو للموظف ", "2023-06-27");
INSERT INTO `expense` VALUES("2", "رواتب", "500", "راتب شهر يناير ", "2023-06-27");
INSERT INTO `expense` VALUES("3", "مصروفات تشغيل", "25", "كلور + برسيل", "2023-06-27");


DROP TABLE IF EXISTS `groups`;
CREATE TABLE `groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `groups` VALUES("1", "كاراتية");
INSERT INTO `groups` VALUES("2", "جمباز");
INSERT INTO `groups` VALUES("3", "جودو ");
INSERT INTO `groups` VALUES("4", "كونغ فو");


DROP TABLE IF EXISTS `info`;
CREATE TABLE `info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `phone` varchar(11) COLLATE utf8_general_mysql500_ci NOT NULL,
  `slogan` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `note1` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `note2` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `info` VALUES("1", "أكاديمية دريم سيبورت", "01020374108", "د/محمد سليمة", "dream academy", "الرياضة غذاء الروح");


DROP TABLE IF EXISTS `invs`;
CREATE TABLE `invs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `invoice` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `invs` VALUES("1", "INV-0000", "2023-06-25");
INSERT INTO `invs` VALUES("2", "INV-00001", "2023-06-25");
INSERT INTO `invs` VALUES("3", "INV-00002", "2023-06-25");
INSERT INTO `invs` VALUES("4", "INV-00003", "2023-06-26");
INSERT INTO `invs` VALUES("5", "INV-00004", "2023-06-27");
INSERT INTO `invs` VALUES("6", "INV-00005", "2023-06-27");
INSERT INTO `invs` VALUES("7", "INV-00006", "2023-06-27");
INSERT INTO `invs` VALUES("8", "INV-00007", "2023-06-27");
INSERT INTO `invs` VALUES("9", "INV-00008", "2023-06-27");
INSERT INTO `invs` VALUES("10", "INV-00009", "2023-06-27");
INSERT INTO `invs` VALUES("11", "INV-00010", "2023-06-27");
INSERT INTO `invs` VALUES("12", "INV-00011", "2023-06-27");
INSERT INTO `invs` VALUES("13", "INV-00012", "2023-06-27");
INSERT INTO `invs` VALUES("14", "INV-00013", "2023-07-11");
INSERT INTO `invs` VALUES("15", "INV-00014", "2023-07-25");
INSERT INTO `invs` VALUES("16", "INV-00015", "2023-07-25");
INSERT INTO `invs` VALUES("17", "INV-00016", "2023-07-25");
INSERT INTO `invs` VALUES("18", "INV-00017", "2023-07-25");
INSERT INTO `invs` VALUES("19", "INV-00018", "2023-07-25");
INSERT INTO `invs` VALUES("20", "INV-00019", "2023-07-25");
INSERT INTO `invs` VALUES("21", "INV-00020", "2023-07-25");
INSERT INTO `invs` VALUES("22", "INV-00021", "2023-07-25");
INSERT INTO `invs` VALUES("23", "INV-00022", "2023-07-25");
INSERT INTO `invs` VALUES("24", "INV-00023", "2023-07-30");


DROP TABLE IF EXISTS `items`;
CREATE TABLE `items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `count` int(3) NOT NULL,
  `price` int(11) NOT NULL,
  `groups` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `items` VALUES("1", "شهر", "14", "150", "كاراتية");
INSERT INTO `items` VALUES("2", "شهر", "13", "140", "جمباز");
INSERT INTO `items` VALUES("3", "سنوية", "150", "300", "جمباز");
INSERT INTO `items` VALUES("4", "تمرين ", "1", "10", "جودو ");
INSERT INTO `items` VALUES("5", "1", "4", "200", "كاراتية");
INSERT INTO `items` VALUES("6", "بسم الله الرحمن الرحيم", "4", "200", "كاراتية");


DROP TABLE IF EXISTS `sessions`;
CREATE TABLE `sessions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `sessions` VALUES("2", "2023-06-27");
INSERT INTO `sessions` VALUES("3", "2023-06-27");
INSERT INTO `sessions` VALUES("4", "2023-06-27");
INSERT INTO `sessions` VALUES("5", "2023-06-27");
INSERT INTO `sessions` VALUES("6", "2023-06-27");
INSERT INTO `sessions` VALUES("7", "2023-06-27");
INSERT INTO `sessions` VALUES("8", "2023-06-27");
INSERT INTO `sessions` VALUES("9", "2023-06-27");
INSERT INTO `sessions` VALUES("10", "2023-07-25");
INSERT INTO `sessions` VALUES("11", "2023-07-25");


DROP TABLE IF EXISTS `signup`;
CREATE TABLE `signup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `last_name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `Phone` varchar(11) COLLATE utf8_general_mysql500_ci NOT NULL,
  `User_name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `user_password` int(1) NOT NULL,
  `reports` int(1) NOT NULL,
  `add_user` int(1) NOT NULL,
  `invoice` int(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `signup` VALUES("1", "ahmed", "1", "a", "admin", "1", "1", "1", "1");


DROP TABLE IF EXISTS `temp_activity`;
CREATE TABLE `temp_activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `trainer` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `category` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `coach` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `date` date NOT NULL,
  `start` varchar(50) COLLATE utf8_general_mysql500_ci NOT NULL,
  `invoice` varchar(11) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



