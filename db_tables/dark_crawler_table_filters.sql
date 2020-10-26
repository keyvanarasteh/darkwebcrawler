
-- --------------------------------------------------------

--
-- Table structure for table `filters`
--

CREATE TABLE `filters` (
  `id` int(11) NOT NULL,
  `key` varchar(100) NOT NULL,
  `regex` bit(1) NOT NULL,
  `fields` varchar(200) NOT NULL,
  `priority` int(11) NOT NULL DEFAULT '0',
  `custom_users` varchar(500) DEFAULT NULL,
  `group` varchar(50) DEFAULT NULL,
  `platform` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `filters`
--

INSERT INTO `filters` (`id`, `key`, `regex`, `fields`, `priority`, `custom_users`, `group`, `platform`) VALUES
(1, 'findgreathomes', b'1', '11111', 49, NULL, NULL, 'dark_tor');
