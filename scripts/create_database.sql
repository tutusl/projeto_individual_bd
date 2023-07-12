SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema evaluatedb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `evaluatedb` ;

-- -----------------------------------------------------
-- Schema evaluatedb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `evaluatedb` ;
USE `evaluatedb` ;


-- -----------------------------------------------------
-- Table `evaluatedb`.`role`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `evaluatedb`.`role` ;

CREATE TABLE IF NOT EXISTS `evaluatedb`.`role` (
  `id` TINYINT NOT NULL AUTO_INCREMENT,
  `label` VARCHAR(45) NOT NULL,
  `name` VARCHAR(90) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `evaluatedb`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `evaluatedb`.`user` ;

CREATE TABLE IF NOT EXISTS `evaluatedb`.`user` (
  `registry` INT(9) NOT NULL,
  `name` VARCHAR(100) NULL DEFAULT NULL,
  `email` VARCHAR(50) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `course` VARCHAR(45) NOT NULL,
  `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `role_id` TINYINT NULL,
  `id` INT NOT NULL AUTO_INCREMENT,
  INDEX `fk_user_1_idx` (`role_id` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_user_1`
    FOREIGN KEY (`role_id`)
    REFERENCES `evaluatedb`.`role` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `evaluatedb`.`department`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `evaluatedb`.`department` ;

CREATE TABLE IF NOT EXISTS `evaluatedb`.`department` (
  `id` INT NOT NULL,
  `name` VARCHAR(150) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `evaluatedb`.`professor`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `evaluatedb`.`professor` ;

CREATE TABLE IF NOT EXISTS `evaluatedb`.`professor` (
  `name` VARCHAR(90) NOT NULL,
  `department_id` INT NOT NULL,
  PRIMARY KEY (`name`, `department_id`),
  INDEX `fk_professor_1_idx` (`department_id` ASC) VISIBLE,
  CONSTRAINT `fk_professor_1`
    FOREIGN KEY (`department_id`)
    REFERENCES `evaluatedb`.`department` (`id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `evaluatedb`.`discipline`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `evaluatedb`.`discipline` ;

CREATE TABLE IF NOT EXISTS `evaluatedb`.`discipline` (
  `discipline_code` VARCHAR(45) NOT NULL,
  `name` VARCHAR(90) NULL,
  `department_id` INT NOT NULL,
  PRIMARY KEY (`discipline_code`),
  INDEX `fk_discipline_1_idx` (`department_id` ASC) VISIBLE,
  CONSTRAINT `fk_discipline_1`
    FOREIGN KEY (`department_id`)
    REFERENCES `evaluatedb`.`department` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `evaluatedb`.`lecture`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `evaluatedb`.`lecture` ;

CREATE TABLE IF NOT EXISTS `evaluatedb`.`lecture` (
  `discipline_code` VARCHAR(45) NOT NULL,
  `class_number` VARCHAR(45) NOT NULL,
  `period` VARCHAR(45) NOT NULL,
  `time` VARCHAR(45) NULL,
  `local` VARCHAR(45) NULL,
  `professor_name` VARCHAR(90) NOT NULL,
  INDEX `fk_class_2_idx` (`professor_name` ASC) VISIBLE,
  INDEX `fk_class_1_idx` (`discipline_code` ASC) VISIBLE,
  INDEX `fk_class_3_idx` (`class_number` ASC) VISIBLE,
  INDEX `fk_class_4_idx` (`period` ASC) VISIBLE,
  PRIMARY KEY (`discipline_code`, `class_number`, `period`),
  CONSTRAINT `fk_class_1`
    FOREIGN KEY (`discipline_code`)
    REFERENCES `evaluatedb`.`discipline` (`discipline_code`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_class_2`
    FOREIGN KEY (`professor_name`)
    REFERENCES `evaluatedb`.`professor` (`name`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `evaluatedb`.`evaluation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `evaluatedb`.`evaluation` ;

CREATE TABLE IF NOT EXISTS `evaluatedb`.`evaluation` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `rating` INT(2) NOT NULL,
  `description` VARCHAR(45) NOT NULL,
  `user_id` INT(9) NOT NULL,
  `class_discipline_code` VARCHAR(45) NOT NULL,
  `class_number` VARCHAR(45) NOT NULL,
  `class_period` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_evaluation_1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_evaluation_2_idx` (`class_discipline_code` ASC) VISIBLE,
  INDEX `fk_evaluation_4_idx` (`class_period` ASC) VISIBLE,
  INDEX `fk_evaluation_3_idx` (`class_number` ASC) VISIBLE,
  CONSTRAINT `fk_evaluation_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `evaluatedb`.`user` (`id`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_evaluation_2`
    FOREIGN KEY (`class_discipline_code`)
    REFERENCES `evaluatedb`.`lecture` (`discipline_code`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_evaluation_3`
    FOREIGN KEY (`class_number`)
    REFERENCES `evaluatedb`.`lecture` (`class_number`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_evaluation_4`
    FOREIGN KEY (`class_period`)
    REFERENCES `evaluatedb`.`lecture` (`period`)
    ON DELETE RESTRICT
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `evaluatedb`.`report`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `evaluatedb`.`report` ;

CREATE TABLE IF NOT EXISTS `evaluatedb`.`report` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `reason` VARCHAR(45) NULL,
  `evaluation_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_report_1_idx` (`evaluation_id` ASC) VISIBLE,
  CONSTRAINT `fk_report_1`
    FOREIGN KEY (`evaluation_id`)
    REFERENCES `evaluatedb`.`evaluation` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
