DROP TABLE IF EXISTS `app_data`;
CREATE TABLE `app_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `confirm` int(5) NOT NULL,
  `barcode_mode` int(5) NOT NULL,
  `trial` int(1) NOT NULL,
  `start_trial` varbinary(255) NOT NULL,
  `finish_trial` varbinary(255) NOT NULL,
  `activation_code` varbinary(255) NOT NULL,
  `weight` int(2) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `app_data` VALUES("1", "0", "0", "1", "b'gAAAAABh7-VQ4bNXSko0x2QS-hTXuNJ89ecm5L0V64aIrCpoKLB6dcCymsbRkELZ6fPmP1tEpoJjfftHXTDegjwlhUmnphSSYg=='", "b'gAAAAABh-xX5KhLKUZJrSh8qjEAWdPOhFQJy2p2TsdUK45e6kh8n-9GVT8LYoL1Juee8jw3qEThgJ5sJEKPw7TL6iIR-9fNhbg=='", "b'gAAAAABh-xX5xvUie6bF1MqY9zVCopvoeFcL8ldu_98Oktn6lrIAwNIpXbByj1ytxeI7UeYdom6P1wlyfcSGReF2kW7NAQg9LOObHepQyaIhjPqQgUWXSwM='", "0");


DROP TABLE IF EXISTS `b2b_accounts`;
CREATE TABLE `b2b_accounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `phone` varchar(11) COLLATE utf8_general_mysql500_ci NOT NULL,
  `total` float(11,0) NOT NULL,
  `paid` float(11,0) NOT NULL DEFAULT 0,
  `remain` float(11,0) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;


DROP TABLE IF EXISTS `b2c_accounts`;
CREATE TABLE `b2c_accounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `phone` varchar(11) COLLATE utf8_general_mysql500_ci NOT NULL,
  `paid` float(10,2) NOT NULL,
  `remain` float(10,2) NOT NULL,
  `total` float(10,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



DROP TABLE IF EXISTS `back_items`;
CREATE TABLE `back_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `recipt` int(11) NOT NULL,
  `item` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `count` float(11,2) NOT NULL,
  `price` float(11,2) NOT NULL,
  `recipt_date` date NOT NULL,
  `purchase_invoice` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;


DROP TABLE IF EXISTS `back_no`;
CREATE TABLE `back_no` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `recipt` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `back_no` VALUES("1", "0");
INSERT INTO `back_no` VALUES("2", "1");


DROP TABLE IF EXISTS `back_recipt`;
CREATE TABLE `back_recipt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `recipt` int(11) NOT NULL,
  `supplier` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `total` float(11,2) NOT NULL,
  `action` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `recipt_date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



DROP TABLE IF EXISTS `back_sales`;
CREATE TABLE `back_sales` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `count` float(11,2) NOT NULL,
  `price` float(11,2) NOT NULL,
  `total` float(11,2) NOT NULL,
  `sales_invoice` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `back_date` date NOT NULL ,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;


DROP TABLE IF EXISTS `barcodes`;
CREATE TABLE `barcodes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bars` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



DROP TABLE IF EXISTS `big_item`;
CREATE TABLE `big_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `item` (`item`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `phone` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



DROP TABLE IF EXISTS `daily_sales`;
CREATE TABLE `daily_sales` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `count` float(10,2) NOT NULL,
  `item_name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `price` float(10,2) NOT NULL,
  `total` float(10,2) NOT NULL,
  `date` date NOT NULL,
  `stat` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `invoice` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `profit` float(10,2) NOT NULL,
  `discount` float(11,2) NOT NULL DEFAULT 0.00,
  `customer` varchar(255) COLLATE utf8_general_mysql500_ci DEFAULT NULL,
  `phone` varchar(11) COLLATE utf8_general_mysql500_ci DEFAULT NULL,
  `stock` varchar(100) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

DROP TABLE IF EXISTS `debt`;
CREATE TABLE `debt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `invoice` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `phone` varchar(11) COLLATE utf8_general_mysql500_ci NOT NULL,
  `paid` float(11,2) NOT NULL,
  `allmoney` float(11,2) NOT NULL,
  `remain` float(11,2) NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



DROP TABLE IF EXISTS `expense`;
CREATE TABLE `expense` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `price` float(11,2) NOT NULL,
  `status` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



DROP TABLE IF EXISTS `groups`;
CREATE TABLE `groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



DROP TABLE IF EXISTS `info`;
CREATE TABLE `info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `address` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `phone` varchar(11) COLLATE utf8_general_mysql500_ci NOT NULL,
  `addition` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `mail` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `slogan` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL DEFAULT '  ',
  `slogan_2` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL DEFAULT '  ',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `info` VALUES("1", "proastica", "shuhadaa", "01020374108", "addition", "aalattar95@gmail.com", "  ", "  ");


DROP TABLE IF EXISTS `invoices`;
CREATE TABLE `invoices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `count` float(11,2) NOT NULL,
  `item_name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `price` float(10,2) NOT NULL,
  `total` float(11,2) NOT NULL,
  `date` date NOT NULL,
  `invoice` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;




DROP TABLE IF EXISTS `invs`;
CREATE TABLE `invs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `invoice` varchar(45) COLLATE utf8_general_mysql500_ci NOT NULL,
  `discount` float(10,1) NOT NULL DEFAULT 0.0,
  `invoice_date` date NOT NULL ,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



DROP TABLE IF EXISTS `permissions`;
CREATE TABLE `permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `addItem` int(11) NOT NULL,
  `stock` int(11) NOT NULL,
  `home` int(11) NOT NULL,
  `dailySales` int(11) NOT NULL,
  `reports` int(11) NOT NULL,
  `expense` int(11) NOT NULL,
  `customerPayment` int(11) NOT NULL,
  `invoices` int(11) NOT NULL,
  `editOrder` int(11) NOT NULL,
  `supplierPayment` int(11) NOT NULL,
  `editDeleteItem` int(11) NOT NULL,
  `payLater` int(11) NOT NULL,
  `admin` int(11) NOT NULL,
  `make_order` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `permissions` VALUES("1", "ahmed", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1");


DROP TABLE IF EXISTS `purchase_recipt`;
CREATE TABLE `purchase_recipt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `item_price` float(10,1) NOT NULL,
  `count` float(10,1) NOT NULL,
  `total` float(10,1) NOT NULL,
  `date` date NOT NULL,
  `recipt` varchar(50) COLLATE utf8_general_mysql500_ci NOT NULL,
  `stock` varchar(100) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



DROP TABLE IF EXISTS `recipt`;
CREATE TABLE `recipt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `invoice` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;

INSERT INTO `recipt` VALUES("1", "0");
INSERT INTO `recipt` VALUES("2", "1");


DROP TABLE IF EXISTS `recipt_pay`;
CREATE TABLE `recipt_pay` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `invoice` varchar(11) COLLATE utf8_general_mysql500_ci NOT NULL,
  `pay_date` date NOT NULL,
  `total` float(10,1) NOT NULL,
  `paid` float(10,1) NOT NULL,
  `remain` float(10,1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



DROP TABLE IF EXISTS `recipts`;
CREATE TABLE `recipts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `invoice` varchar(11) COLLATE utf8_general_mysql500_ci NOT NULL,
  `invoice_date` date NOT NULL,
  `total` float(10,1) NOT NULL,
  `paid` float(10,1) NOT NULL,
  `remain` float(10,1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



DROP TABLE IF EXISTS `salesdebts`;
CREATE TABLE `salesdebts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `invoice` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `phone` varchar(11) COLLATE utf8_general_mysql500_ci NOT NULL,
  `paid` float(11,2) NOT NULL,
  `allMoney` float(11,2) NOT NULL,
  `remain` float(11,2) NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



DROP TABLE IF EXISTS `signup`;
CREATE TABLE `signup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `last_name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `Phone` varchar(11) COLLATE utf8_general_mysql500_ci NOT NULL,
  `user_name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  `user_password` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



DROP TABLE IF EXISTS `small_item`;
CREATE TABLE `small_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



DROP TABLE IF EXISTS `stock`;
CREATE TABLE `stock` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



DROP TABLE IF EXISTS `sus_invoice`;
CREATE TABLE `sus_invoice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `recipt` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



DROP TABLE IF EXISTS `suspesion`;
CREATE TABLE `suspesion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `count` float(10,2) NOT NULL,
  `item_id` int(11) NOT NULL,
  `price` float(11,2) NOT NULL,
  `total` float(11,2) NOT NULL,
  `customer` varchar(255) COLLATE utf8_general_mysql500_ci NOT NULL DEFAULT '  ',
  `suspession_recipt` varchar(2) COLLATE utf8_general_mysql500_ci NOT NULL,
  `discount` float(10,0) NOT NULL DEFAULT 0,
  `size` varchar(50) COLLATE utf8_general_mysql500_ci NOT NULL DEFAULT ' ',
  `stock` varchar(100) COLLATE utf8_general_mysql500_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8 COLLATE=utf8_general_mysql500_ci;



