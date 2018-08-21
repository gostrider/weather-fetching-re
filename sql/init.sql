CREATE TABLE `weather` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `temp` decimal(5,2) DEFAULT NULL,
  `temp_min` smallint(6) DEFAULT NULL,
  `temp_max` smallint(6) DEFAULT NULL,
  `humidity` smallint(6) DEFAULT NULL,
  `city` char(2) DEFAULT NULL,
  `dt` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
