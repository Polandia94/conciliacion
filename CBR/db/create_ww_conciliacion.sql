CREATE OR REPLACE VIEW public.vw_conciliacion
 AS
 SELECT row_number() OVER (ORDER BY main."fechatrabco", main."horatrabco") AS id,
    main."IDRENC",
    main."IDRBCOD_BCO",
    main."fechatrabco",
    main."horatrabco",
    main."debebco",
    main."haberbco",
    main."saldobco",
    main."oficinabco",
    main."desctrabco",
    main."reftrabco",
    main."codtrabco",
    main."IDRERPD_ERP",
    main."nrotraerp",
    main."fechatraerp",
    main."nrocomperp",
    main."auxerp",
    main."referp",
    main."glosaerp",
    main."debeerp",
    main."habererp",
    main."saldoerp",
    main."FECHACON_ERP",
    main.isconciliado,
    main.numrec
   FROM ( SELECT bco."IDRENC",
            bco."IDRBCOD" AS "IDRBCOD_BCO",
            bco."FECHATRA" AS "fechatrabco",
            bco."HORATRA" AS "horatrabco",
            bco."DEBE" AS "debebco",
            bco."HABER" AS "haberbco",
            bco."SALDO" AS "saldobco",
            bco."OFICINA" AS "oficinabco",
            bco."DESCTRA" AS "desctrabco",
            bco."REFTRA" AS "reftrabco",
            bco."CODTRA" AS "codtrabco",
            erp."IDRERPD" AS "IDRERPD_ERP",
            erp."NROTRA" AS "nrotraerp",
            erp."FECHATRA" AS "fechatraerp",
            erp."NROCOMP" AS "nrocomperp",
            erp."AUX" AS "auxerp",
            erp."REF" AS "referp",
            erp."GLOSA" AS "glosaerp",
            erp."DEBE" AS "debeerp",
            erp."HABER" AS "habererp",
            erp."SALDO" AS "saldoerp",
            erp."FECHACON" AS "FECHACON_ERP",
            2 AS isconciliado,
            1 AS numrec
           FROM "CBRBCOD" bco
             JOIN "CBRERPD" erp ON erp."IDRENC" = bco."IDRENC" AND erp."FECHATRA" = bco."FECHATRA" AND erp."DEBE" = bco."DEBE" AND erp."HABER" = bco."HABER"
          WHERE NOT (bco."IDRBCOD" IN ( SELECT rep."IDRBCOD"
                   FROM ( SELECT bco_1."IDRBCOD",
                            bco_1."IDRENC",
                            count(1) AS count
                           FROM "CBRBCOD" bco_1,
                            "CBRERPD" erp_1
                          WHERE bco_1."IDRENC" = erp_1."IDRENC" AND bco_1."FECHATRA" = erp_1."FECHATRA" AND bco_1."DEBE" = erp_1."DEBE" AND bco_1."HABER" = erp_1."HABER"
                          GROUP BY bco_1."IDRBCOD", bco_1."IDRENC", bco_1."FECHATRA", bco_1."DEBE", bco_1."HABER"
                         HAVING count(1) > 1) rep
                  WHERE rep."IDRENC" = bco."IDRENC"))
        UNION
         SELECT erp."IDRENC",
            0,
            NULL::date AS date,
            NULL::time without time zone AS "time",
            0,
            0,
            0,
            NULL::character varying AS "varchar",
            NULL::character varying AS "varchar",
            NULL::character varying AS "varchar",
            NULL::character varying AS "varchar",
            erp."IDRERPD",
            erp."NROTRA",
            erp."FECHATRA" AS "fechatraerp",
            erp."NROCOMP",
            erp."AUX",
            erp."REF",
            erp."GLOSA",
            erp."DEBE" AS "debeerp",
            erp."HABER" AS "habererp",
            erp."SALDO" AS "saldoerp",
            erp."FECHACON" AS "FECHACON_ERP",
            1 AS isconciliado,
            1 AS numrec
           FROM "CBRERPD" erp
          WHERE NOT (erp."IDRENC" IN ( SELECT bco."IDRENC"
                   FROM "CBRBCOD" bco
                  WHERE erp."IDRENC" = bco."IDRENC" AND erp."FECHATRA" = bco."FECHATRA" AND erp."DEBE" = bco."DEBE" AND erp."HABER" = bco."HABER"))
        UNION
         SELECT bco."IDRENC",
            bco."IDRBCOD",
            bco."FECHATRA" AS "fechatrabco",
            bco."HORATRA",
            bco."DEBE" AS "debebco",
            bco."HABER" AS "haberbco",
            bco."SALDO" AS "saldobco",
            bco."OFICINA",
            bco."DESCTRA",
            bco."REFTRA",
            bco."CODTRA",
            0 AS "IDRERPD",
            0 AS "NROTRA",
            NULL::date AS "fechatraerp",
            0 AS "NROCOMP",
            0 AS "AUX",
            NULL::character varying AS "REF",
            NULL::character varying AS "GLOSA",
            0 AS "debeerp",
            0 AS "habererp",
            0 AS "saldoerp",
            NULL::date AS "FECHACON_ERP",
            1 AS isconciliado,
            1 AS numrec
           FROM "CBRBCOD" bco
          WHERE NOT (bco."IDRENC" IN ( SELECT erp."IDRENC"
                   FROM "CBRERPD" erp
                  WHERE erp."IDRENC" = bco."IDRENC" AND erp."FECHATRA" = bco."FECHATRA" AND erp."DEBE" = bco."DEBE" AND erp."HABER" = bco."HABER"))
        UNION
         SELECT bco."IDRENC",
            bco."IDRBCOD",
            bco."FECHATRA" AS "fechatrabco",
            bco."HORATRA",
            bco."DEBE" AS "debebco",
            bco."HABER" AS "haberbco",
            bco."SALDO" AS "saldobco",
            bco."OFICINA",
            bco."DESCTRA",
            bco."REFTRA",
            bco."CODTRA",
            0 AS "IDRERPD",
            0 AS "NROTRA",
            NULL::date AS "fechatraerp",
            0 AS "NROCOMP",
            0 AS "AUX",
            NULL::character varying AS "REF",
            NULL::character varying AS "GLOSA",
            0 AS "debeerp",
            0 AS "habererp",
            0 AS "saldoerp",
            NULL::date AS "FECHACON_ERP",
            2 AS isconciliado,
            ( SELECT count(1) AS count
                   FROM "CBRBCOD" bco_rep
                  WHERE bco_rep."IDRENC" = bco."IDRENC" AND bco_rep."FECHATRA" = bco."FECHATRA" AND bco_rep."DEBE" = bco."DEBE" AND bco_rep."HABER" = bco."HABER") AS numrec
           FROM "CBRBCOD" bco
          WHERE (bco."IDRBCOD" IN ( SELECT rep."IDRBCOD"
                   FROM ( SELECT bco_1."IDRBCOD",
                            count(1) AS count
                           FROM "CBRBCOD" bco_1,
                            "CBRERPD" erp
                          WHERE bco_1."IDRENC" = erp."IDRENC" AND bco_1."FECHATRA" = erp."FECHATRA" AND bco_1."DEBE" = erp."DEBE" AND bco_1."HABER" = erp."HABER"
                          GROUP BY bco_1."IDRBCOD", bco_1."FECHATRA", bco_1."DEBE", bco_1."HABER"
                         HAVING count(1) > 1) rep
                  WHERE bco."IDRBCOD" = rep."IDRBCOD"))
        UNION
         SELECT erp."IDRENC",
            0,
            NULL::date AS date,
            NULL::time without time zone AS "time",
            0,
            0,
            0,
            NULL::character varying AS "varchar",
            NULL::character varying AS "varchar",
            NULL::character varying AS "varchar",
            NULL::character varying AS "varchar",
            erp."IDRERPD",
            erp."NROTRA",
            erp."FECHATRA" AS "fechatraerp",
            erp."NROCOMP",
            erp."AUX",
            erp."REF",
            erp."GLOSA",
            erp."DEBE" AS "debeerp",
            erp."HABER" AS "habererp",
            erp."SALDO" AS "saldoerp",
            erp."FECHACON" AS "FECHACON_ERP",
            2 AS isconciliado,
            ( SELECT count(1) AS count
                   FROM "CBRERPD" erp_rep
                  WHERE erp_rep."IDRENC" = erp."IDRENC" AND erp_rep."FECHATRA" = erp."FECHATRA" AND erp_rep."DEBE" = erp."DEBE" AND erp_rep."HABER" = erp."HABER") AS numrec
           FROM "CBRERPD" erp
          WHERE (erp."IDRERPD" IN ( SELECT rep."IDRERPD"
                   FROM ( SELECT erp_1."IDRERPD",
                            count(1) AS count
                           FROM "CBRBCOD" bco,
                            "CBRERPD" erp_1
                          WHERE bco."IDRENC" = erp_1."IDRENC" AND bco."FECHATRA" = erp_1."FECHATRA" AND bco."DEBE" = erp_1."DEBE" AND bco."HABER" = erp_1."HABER"
                          GROUP BY erp_1."IDRERPD", erp_1."FECHATRA", erp_1."DEBE", erp_1."HABER"
                         HAVING count(1) > 1) rep
                  WHERE rep."IDRERPD" = erp."IDRERPD"))) main
  ORDER BY main."fechatrabco", main."horatrabco";

ALTER TABLE public.vw_conciliacion
    OWNER TO postgres;