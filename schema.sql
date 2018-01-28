-- DB Schema

-- 'found' table
create table found (
    private_key_hex text primary key,
    private_key_wif text,
    public_key_hex  text,
    wallet_address  text,
    hash160         text,
    found_timestamp text
);

-- 'failed' table
create table failed (
    private_key_hex text primary key,
    private_key_wif text,
    public_key_hex  text,
    wallet_address  text,
    hash160         text,
    failed_timestamp text
);
