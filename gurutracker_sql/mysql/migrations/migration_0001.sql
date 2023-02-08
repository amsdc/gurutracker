CREATE TABLE `tutor` (
	`id` INT PRIMARY KEY AUTO_INCREMENT, -- ID
    `name` VARCHAR(100) NOT NULL, -- tutor name, e.g. Deeksha
    `uidentifier` VARCHAR(50) NOT NULL,
    `subject` VARCHAR(50) NOT NULL,
    `level` VARCHAR(50) DEFAULT "school"
);

CREATE TABLE `assignment` (
    `id` INT PRIMARY KEY AUTO_INCREMENT, -- ID,
    `name` VARCHAR(200), -- assignment name
    `uidentifier` VARCHAR(200) NOT NULL UNIQUE, 
    `type` ENUM("test", "worksheet", "summary") NOT NULL DEFAULT "summary",
    `tid` INT, -- tutor id
    CONSTRAINT FK_TutorID FOREIGN KEY (`tid`) REFERENCES 
    `tutor`(`id`) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE `tag` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `text` VARCHAR(100) NOT NULL
);

CREATE TABLE `assignment_tag` (
    `assignment_id` INT,
    `tag_id` INT,
    CONSTRAINT FK_AssignmentTag_Assignment FOREIGN KEY (`assignment_id`)
    REFERENCES `assignment`(`id`),
    CONSTRAINT FK_AssignmentTag_Tag FOREIGN KEY (`tag_id`)
    REFERENCES `tag`(`id`)
);