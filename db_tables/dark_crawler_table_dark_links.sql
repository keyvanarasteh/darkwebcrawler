
-- --------------------------------------------------------

--
-- Table structure for table `dark_links`
--

CREATE TABLE `dark_links` (
  `id` int(11) NOT NULL,
  `url` varchar(150) NOT NULL,
  `crawl_depth` int(11) NOT NULL DEFAULT '0',
  `crawl_allowed` text,
  `crawl_rejected` text,
  `crawl_period` smallint(6) NOT NULL DEFAULT '60',
  `crawl_last` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `checksum` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `dark_links`
--

INSERT INTO `dark_links` (`id`, `url`, `crawl_depth`, `crawl_allowed`, `crawl_rejected`, `crawl_period`, `crawl_last`, `checksum`) VALUES
(1, 'http://4m6omb3gmrmnwzxi.onion/last.php', 0, 'a[href^="show.php?md5="]', NULL, 1, '2018-11-21 09:29:11', '1513462537'),
(2, 'http://pasternjaui2k53d.onion/', 0, NULL, NULL, 1, '2018-11-21 09:29:07', '2102744099');
