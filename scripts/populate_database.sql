INSERT INTO evaluatedb.department (id, name)
VALUES 
	(643, 'CENTRO DE APOIO AO DESENVOLVIMENTO TECNOLÓGICO - BRASÍLIA'),
	(640, 'CENTRO DE DESENVOLVIMENTO SUSTENTÁVEL - BRASÍLIA'),
	(314, 'CENTRO DE EXCELÊNCIA EM TURISMO - BRASÍLIA');
    
INSERT INTO evaluatedb.discipline (discipline_code, name, department_id)
VALUES 
	('CDT1101', 'TECNOLOGIA SOCIAL E INOVAÇÃO', 643),
    ('CDS0004', 'AGRICULTURA E MEIO AMBIENTE', 640),
    ('CDS0007', 'INTRODUÇÃO AO DESENVOLVIMENTO SUSTENTÁVEL', 640),
    ('CET0013', 'INTRODUÇÃO AO PESQUISA EM TURISMO SUSTENTÁVEL', 314);
    
INSERT INTO evaluatedb.professor (name, department_id)
VALUES 
	('ADRILANE BATISTA DE OLIVEIRA (60h)', 640),
	('JONATHAS FELIPE AIRES FERREIRA (30h)', 643),
	('TANIA CRISTINA DA SILVA CRUZ (30h)', 643),
    ('MAURO GUILHERME MAIDANA CAPPELLARO (60h)', 640),
    ('MARUTSCHKA MARTINI MOESCH (30h)', 314),
    ('MARUTSCHKA MARTINI MOESCH (60h)', 314);

INSERT INTO evaluatedb.lecture (discipline_code, class_number, period, time, local, professor_name)
VALUES 
	('CDS0007', '4', '2023.1', '36N12', 'ICC AT 158/19 (50)', 'ADRILANE BATISTA DE OLIVEIRA (60h)'),
	('CDS0007', '3', '2023.1', '36N12', 'ICC AT 158/19 (50)', 'MAURO GUILHERME MAIDANA CAPPELLARO (60h)'),
	('CDT1101', '1', '2023.1', '36N12', 'ICC AT 158/19 (50)', 'TANIA CRISTINA DA SILVA CRUZ (30h)'),
    ('CDT1101', '1', '2022.2', '36N12', 'ICC AT 158/19 (50)', 'TANIA CRISTINA DA SILVA CRUZ (30h)'),
    ('CDT1101', '1', '2022.2', '36N12', 'ICC AT 158/19 (50)', 'JONATHAS FELIPE AIRES FERREIRA (30h)'),
	('CET0013', '1', '2022.1', '3M1234', 'CET - Módulo E', 'MARUTSCHKA MARTINI MOESCH (60h)'),
    ('CDT1101', '1', '2022.1', '6T2345', 'Local à definir.', 'TANIA CRISTINA DA SILVA CRUZ (30h)'),
    ('CDS0007', '1', '2022.1', '36N12', 'ICC AT 158/19 (50)', 'MAURO GUILHERME MAIDANA CAPPELLARO (60h)');

INSERT INTO evaluatedb.role (label, name)
VALUES 
	('admin', 'admin_user'),
    ('std', 'standard_user');

INSERT INTO evaluatedb.user (registry, name, email, password, course, role_id)
VALUES 
	(111222333, 'arthur', 'arthur@gmail.com', 'aaa', 'computacao', 1),
    (444555666, 'exemplo1', 'exemplo1@gmail.com', 'bbb', 'computacao', 2),
    (777888999, 'exemplo2', 'exemplo2@gmail.com', 'ccc', 'computacao', 2);
    