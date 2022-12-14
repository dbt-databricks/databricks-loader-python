/* Replace with your SQL commands */
CREATE TABLE opensea_trades (
    tx_hash char(66) NOT NULL,
    blockchain varchar(24),
    platform varchar(24),
    nft_token_id varchar(64),
    exchange_contract_address varchar(42),
    nft_contract_address varchar(42),
    erc_standard varchar(24),
    aggregator varchar(24),
    number_of_items bigint,
    trade_type varchar(32),
    buyer varchar(42),
    seller varchar(42),
    nft_project_name text,
    currency_amount double precision,
    usd_amount double precision,
    eth_amount double precision,
    original_currency_amount double precision,
    currency_symbol varchar(24),
    currency_contract varchar(42),
    original_currency_contract varchar(42),
    block_time timestamp NOT NULL,
    block_number bigint,
    tx_from varchar(42),
    tx_to varchar(42)
);