
-- --------------------------------------------------------

--
-- Table structure for table `dark_link_rules`
--

CREATE TABLE `dark_link_rules` (
  `id` int(11) NOT NULL,
  `url_pattern` varchar(150) NOT NULL,
  `crawl_allowed` text,
  `crawl_rejected` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `dark_link_rules`
--

INSERT INTO `dark_link_rules` (`id`, `url_pattern`, `crawl_allowed`, `crawl_rejected`) VALUES
(1, 'show\\.php\\?md5=', 'h3,textarea', NULL);
