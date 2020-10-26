
-- --------------------------------------------------------

--
-- Table structure for table `dark_links_checksum`
--

CREATE TABLE `dark_links_checksum` (
  `id` int(11) NOT NULL,
  `url` varchar(500) NOT NULL,
  `crawl_last` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `checksum` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `dark_links_checksum`
--

INSERT INTO `dark_links_checksum` (`id`, `url`, `crawl_last`, `checksum`) VALUES
(1, 'http://4m6omb3gmrmnwzxi.onion/show.php?md5=f1eba4f4103ee7487391a9187499ad47', '2018-08-14 07:32:45', '885184591');
