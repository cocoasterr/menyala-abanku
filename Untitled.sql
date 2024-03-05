-- Create the "users" table
CREATE TABLE IF NOT EXISTS "users" (
  "id" varchar PRIMARY KEY,
  "nomor_rekening" varchar,
  "phone_number" varchar,
  "nik" varchar,
  "pin" varchar,
  "saldo" int
);

CREATE INDEX IF NOT EXISTS idx_users_id ON "users" ("id");
CREATE INDEX IF NOT EXISTS idx_users_nomor_rekening ON "users" ("nomor_rekening");

-- Create the "mutation" table
CREATE TABLE IF NOT EXISTS "mutation" (
  "id" varchar PRIMARY KEY,
  "nomor_rekening" varchar,
  "transaction_code" varchar CHECK ("transaction_code" IN ('C', 'D', 'T','U')),
  "time" varchar,
  "nominal" varchar
);

CREATE INDEX IF NOT EXISTS idx_mutation_id ON "mutation" ("id");
CREATE INDEX IF NOT EXISTS idx_mutation_nomor_rekening ON "mutation" ("nomor_rekening");
