CREATE DATABASE `cosmetice`;
use `cosmetice`;
#drop database cosmetice;
CREATE TABLE `cosmetice`.`clienti` (
  `idclient` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) ,
  `password` VARCHAR(45) ,
  `nr_tel` VARCHAR(45) ,
  PRIMARY KEY (`idclient`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) , -- username-ul este unic in baza de date, in ordine ascendenta
  UNIQUE INDEX `nr_tel_UNIQUE` (`nr_tel` ASC) );	-- nr_tel este unic in baza de date, in ordine ascendenta
  
  DESCRIBE clienti;
  
  CREATE TABLE `cosmetice`.`produse` (
  `idprodus` INT NOT NULL AUTO_INCREMENT,
  `pret` FLOAT,
  `nume` VARCHAR(200),
  `brand` VARCHAR(150),
  PRIMARY KEY (`idprodus`),
  UNIQUE INDEX `nume_UNIQUE` (`nume` ASC) );
  
    DESCRIBE produse;
    
  CREATE TABLE `cosmetice`.`cos` (
  `idcos` INT NOT NULL AUTO_INCREMENT,
  `idprodus` INT ,
  `idclient` INT NOT NULL,
  PRIMARY KEY (`idcos`));
  
    DESCRIBE cos;
  
  CREATE TABLE `cosmetice`.`comenzi` (
    `idcomanda` INT NOT NULL AUTO_INCREMENT,
    `idcurier` INT NOT NULL,
    `idclient` INT NOT NULL,
    `status` VARCHAR(45),
    `pret_comanda` FLOAT,
    `adresa` VARCHAR(150),
    PRIMARY KEY (`idcomanda`)
);

  DESCRIBE comenzi;
  
  
  CREATE TABLE `cosmetice`.`curieri` (
  `idcurier` INT NOT NULL AUTO_INCREMENT,
  `nume` VARCHAR(45) ,
  `nr_tel` VARCHAR(45) ,
  `status` VARCHAR(45) ,
  PRIMARY KEY (`idcurier`),
  UNIQUE INDEX `nume_UNIQUE` (`nume` ASC) ,
  UNIQUE INDEX `nr_tel_UNIQUE` (`nr_tel` ASC) );
  
    DESCRIBE curieri;
  
ALTER TABLE `cosmetice`.`cos` 
ADD CONSTRAINT `idprodus`
  FOREIGN KEY (`idprodus`)
  REFERENCES `cosmetice`.`produse` (`idprodus`)
  ON DELETE CASCADE,
ADD CONSTRAINT `idclient`
  FOREIGN KEY (`idclient`)
  REFERENCES `cosmetice`.`clienti` (`idclient`)
  ON DELETE CASCADE;


ALTER TABLE `cosmetice`.`comenzi` 
ADD CONSTRAINT `idclient2`
  FOREIGN KEY (`idclient`)
  REFERENCES `cosmetice`.`clienti` (`idclient`)
  ON DELETE CASCADE,
ADD CONSTRAINT `idcurier`
  FOREIGN KEY (`idcurier`)
  REFERENCES `cosmetice`.`curieri` (`idcurier`)
  ON DELETE CASCADE;

DELIMITER $$

CREATE PROCEDURE add_client (
    IN p_username VARCHAR(45),
    IN p_password VARCHAR(45),
    IN p_nr_tel VARCHAR(45)
)
BEGIN
    -- Verificăm dacă numărul de telefon are exact 10 cifre
    IF LENGTH(p_nr_tel) != 10 OR p_nr_tel NOT REGEXP '^[0-9]+$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Numărul de telefon trebuie să aibă exact 10 cifre';
    ELSE
        -- Inserăm clientul în baza de date
        INSERT INTO clienti (username, password, nr_tel)
        VALUES (p_username, p_password, p_nr_tel);
    END IF;
END $$

DELIMITER ;

DELIMITER //

CREATE TRIGGER check_pret_interval
BEFORE INSERT ON produse
FOR EACH ROW
BEGIN
    IF NEW.pret < 0 OR NEW.pret > 1000 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Valoarea pentru pret trebuie sa fie intre 0 si 1000';
    END IF;
END $$

DELIMITER ;

INSERT INTO `cosmetice`.`produse` (`pret`, `nume`, `brand`) VALUES ('170', 'Sultry Mini Eyeshadow Palette', 'Huda Beauty');
INSERT INTO `cosmetice`.`produse` (`pret`, `nume`, `brand`) VALUES ('135', 'Kit 3 produse pentru buze', 'Sephora');
INSERT INTO `cosmetice`.`produse` (`pret`, `nume`, `brand`) VALUES ('230', 'Set produse pentru sprancene', 'Benefit');
INSERT INTO `cosmetice`.`produse` (`pret`, `nume`, `brand`) VALUES ('25', 'Gloss de buze', 'Sephora');
INSERT INTO `cosmetice`.`produse` (`pret`, `nume`, `brand`) VALUES ('209', 'Easy Bake Loose Powder - Pudra libera', 'Huda Beauty');
INSERT INTO `cosmetice`.`produse` (`pret`, `nume`, `brand`) VALUES ('150', ' Stick pentru conturul fetei', 'Rare Beauty');
INSERT INTO `cosmetice`.`produse` (`pret`, `nume`, `brand`) VALUES ('165', ' Mascara pentru volum', 'Too Faced');
INSERT INTO `cosmetice`.`produse` (`pret`, `nume`, `brand`) VALUES ('299', 'Dior Backstage Eye Palette - Paleta farduri de pleoape', 'Dior');
INSERT INTO `cosmetice`.`produse` (`pret`, `nume`, `brand`) VALUES ('110', 'Artist Color Pencil - Creion multifunctional', 'Make Up For Ever');
INSERT INTO `cosmetice`.`produse` (`pret`, `nume`, `brand`) VALUES ('130', 'Aqua Resist Color Ink - Eyeliner', 'Make Up For Ever');
INSERT INTO `cosmetice`.`produse` (`pret`, `nume`, `brand`) VALUES ('230', 'Baby Bronze - Paleta farduri de pleoape', 'Natasha Denona');
INSERT INTO `cosmetice`.`produse` (`pret`, `nume`, `brand`) VALUES ('167', 'Tattoo Liner - Tus pentru conturul ochilor', 'KVD Beauty');
INSERT INTO `cosmetice`.`produse` (`pret`, `nume`, `brand`) VALUES ('125', 'Inked Up Duo - Set machiaj', 'KVD Beauty');
INSERT INTO `cosmetice`.`produse` (`pret`, `nume`, `brand`) VALUES ('85', 'Midnight Shadows - Fard de pleoape lichid', 'REM Beauty');
INSERT INTO `cosmetice`.`produse` (`pret`, `nume`, `brand`) VALUES ('201', 'Diamond Bomb All-Over Diamond Veil - Iluminator pentru fata si corp', 'Fenty Beauty');



INSERT INTO `cosmetice`.`curieri` (`nume`, `nr_tel`, `status`) VALUES ('marian', '0744519074', 'liber');
INSERT INTO `cosmetice`.`curieri` (`nume`, `nr_tel`, `status`) VALUES ('andrei', '0723428233', 'liber');
INSERT INTO `cosmetice`.`curieri` (`nume`, `nr_tel`, `status`) VALUES ('robert', '0230510073', 'liber');
INSERT INTO `cosmetice`.`curieri` (`nume`, `nr_tel`, `status`) VALUES ('victor', '0722585229', 'liber');
INSERT INTO `cosmetice`.`curieri` (`nume`, `nr_tel`, `status`) VALUES ('vlad', '0241585103', 'liber');
INSERT INTO `cosmetice`.`curieri` (`nume`, `nr_tel`, `status`) VALUES ('alin', '0720996900', 'liber');
INSERT INTO `cosmetice`.`curieri` (`nume`, `nr_tel`, `status`) VALUES ('cosmin', '0256433273', 'liber');
INSERT INTO `cosmetice`.`curieri` (`nume`, `nr_tel`, `status`) VALUES ('marius', '0749017843', 'liber');
INSERT INTO `cosmetice`.`curieri` (`nume`, `nr_tel`, `status`) VALUES ('vasile', '0245227002 ', 'liber');
INSERT INTO `cosmetice`.`curieri` (`nume`, `nr_tel`, `status`) VALUES ('eduard', '0723289964 ', 'liber');



