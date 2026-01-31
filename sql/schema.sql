-- 1. Unidades de Estudo (Agnóstico: qualquer varejo)
CREATE TABLE IF NOT EXISTS tb_unidades_analise (
    id_local SERIAL PRIMARY KEY,
    nome_identificador VARCHAR(255),
    segmento_varejo VARCHAR(100),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    raio_influencia_metros INT DEFAULT 1000
);

-- 2. Camada de Dinâmica Comercial (Concorrência/CNAE)
CREATE TABLE IF NOT EXISTS tb_dinamica_comercial (
    id_ponto SERIAL PRIMARY KEY,
    cnpj VARCHAR(18),
    razao_social VARCHAR(255),
    cnae_codigo VARCHAR(7),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

-- 3. Camada Socioeconômica (IBGE)
CREATE TABLE IF NOT EXISTS tb_demografia_setores (
    cod_setor_censitario VARCHAR(20) PRIMARY KEY,
    populacao_total INT,
    renda_media_mensal DECIMAL(12,2),
    geometria_wkt TEXT
);