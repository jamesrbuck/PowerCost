-- File: Setup_Database.sql

create database pse;

use pse;

select database();
show tables;


CREATE TABLE `pse`.`usage_e` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `UDate` DATE NOT NULL,
  `UTime` TIME NOT NULL,
  `kWh` DECIMAL(7,3) NULL DEFAULT 0.0,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `I_USAGE_E_UNIQUE` (`ID` ASC) VISIBLE)
COMMENT = 'Puget Sound Energy Electricity Usage for The Ponderosa';

-- drop table pse.daily_kwh;
CREATE TABLE `pse`.`daily_kwh` (
  ID INT NOT NULL AUTO_INCREMENT,
  UDate DATE NOT NULL,
  DOW VARCHAR(15) NOT NULL,
  kWh DECIMAL(7,3) NULL DEFAULT 0.0,
  hours INT NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `I_DAILY_KWH_E_UNIQUE` (`ID` ASC) VISIBLE)
COMMENT = 'PSE Daily KWH Usage for The Ponderosa';

CREATE TABLE `pse`.`hourly_kwh` (
  ID INT NOT NULL AUTO_INCREMENT,
  hour INT NOT NULL,
  kWhAvg DECIMAL(7,3) NULL DEFAULT 0.0,
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `I_HOURLY_KWH_E_UNIQUE` (`ID` ASC) VISIBLE)
COMMENT = 'PSE Hourly KWH Usage for The Ponderosa';