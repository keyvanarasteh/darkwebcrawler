
--
-- Indexes for dumped tables
--

--
-- Indexes for table `config`
--
ALTER TABLE `config`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `dark_links`
--
ALTER TABLE `dark_links`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `dark_links_url` (`url`);

--
-- Indexes for table `dark_links_checksum`
--
ALTER TABLE `dark_links_checksum`
  ADD KEY `dark_links_checksum_id` (`id`),
  ADD KEY `dark_links_checksum_url` (`url`(255));

--
-- Indexes for table `dark_link_rules`
--
ALTER TABLE `dark_link_rules`
  ADD PRIMARY KEY (`id`,`url_pattern`);

--
-- Indexes for table `filters`
--
ALTER TABLE `filters`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `dark_links`
--
ALTER TABLE `dark_links`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `dark_links_checksum`
--
ALTER TABLE `dark_links_checksum`
  ADD CONSTRAINT `dark_links_checksum_ibfk_1` FOREIGN KEY (`id`) REFERENCES `dark_links` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `dark_link_rules`
--
ALTER TABLE `dark_link_rules`
  ADD CONSTRAINT `dark_link_rules_ibfk_1` FOREIGN KEY (`id`) REFERENCES `dark_links` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;
