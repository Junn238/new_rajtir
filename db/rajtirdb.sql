-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema rajtir
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema rajtir
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `rajtir` DEFAULT CHARACTER SET utf8mb3 ;
USE `rajtir` ;

-- -----------------------------------------------------
-- Table `rajtir`.`cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rajtir`.`cliente` (
  `Id_cli` INT NOT NULL AUTO_INCREMENT,
  `Nom_cli` VARCHAR(50) NULL DEFAULT NULL,
  `Tip_cli` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`Id_cli`),
  UNIQUE INDEX `Id_cli_UNIQUE` (`Id_cli` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `rajtir`.`empleado`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rajtir`.`empleado` (
  `Id_emp` INT NOT NULL AUTO_INCREMENT,
  `Nom_emp` VARCHAR(50) NOT NULL,
  `Ed_emp` TINYINT NOT NULL,
  `Tel_emp` VARCHAR(15) NOT NULL,
  `Em_emp` VARCHAR(50) NOT NULL,
  `Tie_emp` INT NOT NULL,
  `Tur_emp` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`Id_emp`),
  UNIQUE INDEX `Id_emp_UNIQUE` (`Id_emp` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `rajtir`.`comision`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rajtir`.`comision` (
  `Id_pa` INT NOT NULL AUTO_INCREMENT,
  `Id_emp` INT NOT NULL,
  `Id_cli` INT NOT NULL,
  `Can_pa` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`Id_pa`, `Id_emp`, `Id_cli`),
  UNIQUE INDEX `Id_pa_UNIQUE` (`Id_pa` ASC) VISIBLE,
  INDEX `fk_Empleado_has_Cliente_Cliente1_idx` (`Id_cli` ASC) VISIBLE,
  INDEX `fk_Empleado_has_Cliente_Empleado1_idx` (`Id_emp` ASC) VISIBLE,
  CONSTRAINT `fk_Empleado_has_Cliente_Cliente1`
    FOREIGN KEY (`Id_cli`)
    REFERENCES `rajtir`.`cliente` (`Id_cli`),
  CONSTRAINT `fk_Empleado_has_Cliente_Empleado1`
    FOREIGN KEY (`Id_emp`)
    REFERENCES `rajtir`.`empleado` (`Id_emp`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `rajtir`.`proveedor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rajtir`.`proveedor` (
  `Id_prov` INT NOT NULL AUTO_INCREMENT,
  `Ho_prov` VARCHAR(20) NOT NULL,
  `Nom_prov` VARCHAR(50) NOT NULL,
  `Ubi_pro` VARCHAR(100) NOT NULL,
  `Mar_prov` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`Id_prov`),
  UNIQUE INDEX `Id_pro_UNIQUE` (`Id_prov` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `rajtir`.`producto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rajtir`.`producto` (
  `Id_pro` INT NOT NULL AUTO_INCREMENT,
  `Nom_pro` VARCHAR(50) NOT NULL,
  `Val_pro` DECIMAL(10,2) NOT NULL,
  `Mar_pro` VARCHAR(30) NOT NULL,
  `Can_pro` INT NOT NULL,
  `Des_pro` VARCHAR(255) NOT NULL,
  `Id_prov` INT NOT NULL,
  PRIMARY KEY (`Id_pro`),
  UNIQUE INDEX `Id_pro_UNIQUE` (`Id_pro` ASC) VISIBLE,
  INDEX `fk_proveedor` (`Id_prov` ASC) VISIBLE,
  CONSTRAINT `fk_proveedor`
    FOREIGN KEY (`Id_prov`)
    REFERENCES `rajtir`.`proveedor` (`Id_prov`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `rajtir`.`movimiento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rajtir`.`movimiento` (
  `Id_mov` INT NOT NULL AUTO_INCREMENT,
  `Cliente_Id` INT NOT NULL,
  `Id_pr` INT NOT NULL,
  `Pag_mov` DECIMAL(10,2) NOT NULL,
  `Cam_mov` DECIMAL(10,2) NOT NULL,
  `Fal_mov` DECIMAL(10,2) NOT NULL,
  `Fec_mov` DATETIME NOT NULL,
  `Fin_mov` DATETIME NOT NULL,
  `Tot_mov` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`Id_mov`, `Cliente_Id`, `Id_pr`),
  UNIQUE INDEX `Id_mov_UNIQUE` (`Id_mov` ASC) VISIBLE,
  INDEX `fk_Cliente_has_Producto_Producto1_idx` (`Id_pr` ASC) VISIBLE,
  INDEX `fk_Cliente_has_Producto_Cliente_idx` (`Cliente_Id` ASC) VISIBLE,
  CONSTRAINT `fk_Cliente_has_Producto_Cliente`
    FOREIGN KEY (`Cliente_Id`)
    REFERENCES `rajtir`.`cliente` (`Id_cli`),
  CONSTRAINT `fk_Cliente_has_Producto_Producto1`
    FOREIGN KEY (`Id_pr`)
    REFERENCES `rajtir`.`producto` (`Id_pro`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `rajtir`.`ticket`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rajtir`.`ticket` (
  `Id_tic` INT NOT NULL AUTO_INCREMENT,
  `Id_cli` INT NOT NULL,
  `Id_pro` INT NOT NULL,
  `Pag_tic` DECIMAL(10,2) NOT NULL,
  `Cam_tic` DECIMAL(10,2) NOT NULL,
  `Fal_tic` DECIMAL(10,2) NOT NULL,
  `Fec_tic` DATETIME NOT NULL,
  `Fin_tic` DATETIME NOT NULL,
  `NomSuc_tic` VARCHAR(50) NOT NULL,
  `Hor_tic` TIME NOT NULL,
  PRIMARY KEY (`Id_tic`, `Id_cli`, `Id_pro`),
  UNIQUE INDEX `Id_tic_UNIQUE` (`Id_tic` ASC) VISIBLE,
  INDEX `fk_Cliente_has_Producto_Producto2_idx` (`Id_pro` ASC) VISIBLE,
  INDEX `fk_Cliente_has_Producto_Cliente1_idx` (`Id_cli` ASC) VISIBLE,
  CONSTRAINT `fk_Cliente_has_Producto_Cliente1`
    FOREIGN KEY (`Id_cli`)
    REFERENCES `rajtir`.`cliente` (`Id_cli`),
  CONSTRAINT `fk_Cliente_has_Producto_Producto2`
    FOREIGN KEY (`Id_pro`)
    REFERENCES `rajtir`.`producto` (`Id_pro`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
