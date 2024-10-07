# Sistema-Contable
Este es el repositorio del código del grupo 5 del curso de Sistema y gestión financiera.
Aprovechamos este espacio para detallar los pasos para ejecutar correctamente el programa:
## Paso 1: Crear la Base de datos
### Se tiene que llamar SistemaFinanciero

```sql
DROP TABLE IF EXISTS catalogo_elementos;
DROP TABLE IF EXISTS catalogo_cuentas;
DROP TABLE IF EXISTS libros_diarios;

CREATE TABLE public.catalogo_elementos (
    id_elemento integer NOT NULL,
    nombre text NOT NULL
);

ALTER TABLE ONLY public.catalogo_elementos
    ADD CONSTRAINT catalogo_elementos_pkey PRIMARY KEY (id_elemento);

CREATE TABLE public.catalogo_cuentas (
    id_cuenta integer NOT NULL,
    id_elemento integer NOT NULL,
    nombre text NOT NULL
);

ALTER TABLE ONLY public.catalogo_cuentas
    ADD CONSTRAINT catalogo_cuentas_pkey PRIMARY KEY (id_cuenta);

ALTER TABLE ONLY public.catalogo_cuentas
    ADD CONSTRAINT id_elemento FOREIGN KEY (id_elemento) REFERENCES public.catalogo_elementos(id_elemento);

CREATE TABLE public.libros_diarios (
    id_libro character varying NOT NULL,
    fecha date,
    id_cuenta integer NOT NULL,
    debe numeric,
    haber numeric
);

ALTER TABLE ONLY public.libros_diarios
    ADD CONSTRAINT libros_diarios_pkey PRIMARY KEY (id_libro);
    
ALTER TABLE ONLY public.libros_diarios
    ADD CONSTRAINT id_cuenta FOREIGN KEY (id_cuenta) REFERENCES public.catalogo_cuentas(id_cuenta) NOT VALID;

INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (10, 1, 'Efectivo y equivalentes de efectivo');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (11, 1, 'Inversiones financieras');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (12, 1, 'Cuentas por cobrar comerciales – Terceros');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (13, 1, 'Cuentas por cobrar comerciales – Relacionadas');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (14, 1, 'Cuentas por cobrar al personal, a los accionistas (socios) y directores');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (16, 1, 'Cuentas por cobrar diversas – Terceros');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (17, 1, 'Cuentas por cobrar diversas – Relacionadas');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (18, 1, 'Servicios y otros contratados por anticipado ');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (19, 1, 'Estimación de cuentas de cobranza dudosa');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (20, 2, 'Mercaderías');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (21, 2, 'Productos terminados');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (22, 2, 'Subproductos, desechos y desperdicios');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (23, 2, 'Productos en proceso');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (24, 2, 'Materias primas');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (25, 2, 'Materiales auxiliares, suministros y repuestos');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (26, 2, 'Envases y embalajes');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (27, 2, 'Activos no corrientes mantenidos para la venta');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (28, 2, 'Inventarios por recibir');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (29, 2, 'Desvalorización de inventarios');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (30, 3, 'Inversiones mobiliarias');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (31, 3, 'Propiedades de inversión');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (32, 3, 'Activos por derecho de uso');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (33, 3, 'Propiedad, planta y equipo');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (34, 3, 'Intangibles');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (35, 3, 'Activos biológicos');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (36, 3, 'Desvalorización de activo inmovilizado');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (37, 3, 'Activo diferido');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (38, 3, 'Otros activos');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (39, 3, 'Depreciación y amortización acumulados');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (40, 4, 'Tributos, contraprestaciones y aportes al sistema público de pensiones y de salud por pagar');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (41, 4, 'Remuneraciones y participaciones por pagar');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (42, 4, 'Cuentas por pagar comerciales - Terceros');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (43, 4, 'Cuentas por pagar comerciales - Relacionadas');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (44, 4, 'Cuentas por pagar a los accionistas (socios, partícipes) y directores');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (45, 4, 'Obligaciones financieras');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (46, 4, 'Cuentas por pagar diversas – Terceros');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (47, 4, 'Cuentas por pagar diversas – Relacionadas');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (48, 4, 'Provisiones');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (49, 4, 'Pasivo diferido');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (50, 5, 'Capital');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (51, 5, 'Acciones de inversión');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (52, 5, 'Capital adicional');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (56, 5, 'Resultados no realizados');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (57, 5, 'Excedente de revaluación');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (58, 5, 'Reservas');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (59, 5, 'Resultados acumulados');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (60, 6, 'Compras');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (61, 6, 'Variación de inventarios');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (62, 6, 'Gastos de personal y directores');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (63, 6, 'Gastos de servicios prestados por terceros');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (64, 6, 'Gastos por tributos');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (65, 6, 'Otros gastos de gestión');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (66, 6, 'Pérdida por medición de activos no financieros al valor razonable');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (67, 6, 'Gastos financieros');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (68, 6, 'Valuación y deterioro de activos y provisiones');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (69, 6, 'Costo de ventas');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (70, 7, 'Ventas');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (71, 7, 'Variación de la producción almacenada');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (72, 7, 'Producción de activo inmovilizado');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (73, 7, 'Descuentos, rebajas y bonificaciones obtenidos');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (74, 7, 'Descuentos, rebajas y bonificaciones concedidos');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (75, 7, 'Otros ingresos de gestión');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (76, 7, 'Ganancia por medición de activos no financieros al valor razonable');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (77, 7, 'Ingresos financieros');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (78, 7, 'Cargas cubiertas por provisiones');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (79, 7, 'Cargas imputables a cuentas de costos y gastos');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (80, 8, 'Margen comercial');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (81, 8, 'Producción del ejercicio');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (82, 8, 'Valor agregado');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (83, 8, 'Excedente bruto (insuficiencia bruta) de explotación');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (84, 8, 'Resultado de explotación');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (85, 8, 'Resultado antes de participaciones e impuestos');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (88, 8, 'Impuesto a la renta');
INSERT INTO public.catalogo_cuentas (id_cuenta, id_elemento, nombre) VALUES (89, 8, 'Determinación del resultado del ejercicio');

INSERT INTO public.catalogo_elementos (id_elemento, nombre) VALUES (1, 'EFECTIVO Y EQUIVALENTES DE EFECTIVO');
INSERT INTO public.catalogo_elementos (id_elemento, nombre) VALUES (2, 'ACTIVO REALIZABLE');
INSERT INTO public.catalogo_elementos (id_elemento, nombre) VALUES (3, 'ACTIVO INMOVILIZADO');
INSERT INTO public.catalogo_elementos (id_elemento, nombre) VALUES (4, 'PASIVO');
INSERT INTO public.catalogo_elementos (id_elemento, nombre) VALUES (5, 'PATRIMONIO NETO');
INSERT INTO public.catalogo_elementos (id_elemento, nombre) VALUES (6, 'GASTOS POR NATURALEZA');
INSERT INTO public.catalogo_elementos (id_elemento, nombre) VALUES (7, 'INGRESOS');
INSERT INTO public.catalogo_elementos (id_elemento, nombre) VALUES (8, 'SALDOS INTERMEDIARIOS DE GESTIÓN Y DETERMINACIÓN DEL RESULTADO DEL EJERCICIO');
```
