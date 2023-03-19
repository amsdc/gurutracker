-- New subject table
CREATE TABLE `subject` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL, -- subject name, e.g. Physics 12
    `desc` TEXT, -- description e.g Physics is the study of nature
    `uidentifier` VARCHAR(50) UNIQUE NOT NULL
);

ALTER TABLE `tutor` CHANGE `subject` `subid` INT;
ALTER TABLE `tutor` ADD CONSTRAINT FK_Tutor_Subject 
FOREIGN KEY (`subid`) REFERENCES `subject`(`id`) 
ON UPDATE CASCADE ON DELETE CASCADE;

-- Remove tutor level
-- New subjects can act as levels instead
ALTER TABLE `tutor` DROP `level`; 

-- Add nested tags support
ALTER TABLE `tag` ADD `parent_tag_id` INT;
ALTER TABLE `tag` ADD CONSTRAINT FK_Tag_Tag
FOREIGN KEY (`parent_tag_id`) REFERENCES `tag`(`id`)
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE `tag` MODIFY `text` VARCHAR(50) NOT NULL; -- removed unique restriction to allow nested tags with same names

-- Make tag deletion as cascading
ALTER TABLE `assignment_tag` DROP CONSTRAINT FK_AssignmentTag_Tag;
ALTER TABLE `assignment_tag` ADD CONSTRAINT FK_AssignmentTag_Tag
FOREIGN KEY (`tag_id`) REFERENCES `tag`(`id`) ON UPDATE CASCADE
ON DELETE CASCADE;

-- tutor uid unique
ALTER TABLE `tutor` MODIFY `uidentifier` VARCHAR(50) UNIQUE NOT NULL;