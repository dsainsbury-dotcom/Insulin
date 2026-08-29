-- ICR Meal Dashboard v2.4.1 - cloud food library
-- Run once in Supabase SQL Editor.

create table if not exists public.food_library (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  client_id text not null,
  barcode text,
  name text not null,
  brand text,
  nutrition_source text,
  carbs_100g numeric,
  fat_100g numeric,
  protein_100g numeric,
  kcal_100g numeric,
  serving_weight_g numeric,
  usual_portion_g numeric,
  use_count integer not null default 0,
  last_used_at timestamptz,
  favourite boolean not null default false,
  hidden boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(user_id, client_id)
);

create unique index if not exists food_library_user_barcode_unique
on public.food_library(user_id, barcode)
where barcode is not null and barcode <> '';

alter table public.food_library enable row level security;

drop policy if exists "food_library_select_own" on public.food_library;
create policy "food_library_select_own" on public.food_library
for select using (auth.uid() = user_id);

drop policy if exists "food_library_insert_own" on public.food_library;
create policy "food_library_insert_own" on public.food_library
for insert with check (auth.uid() = user_id);

drop policy if exists "food_library_update_own" on public.food_library;
create policy "food_library_update_own" on public.food_library
for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists "food_library_delete_own" on public.food_library;
create policy "food_library_delete_own" on public.food_library
for delete using (auth.uid() = user_id);

create or replace function public.set_food_library_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists trg_food_library_updated_at on public.food_library;
create trigger trg_food_library_updated_at
before update on public.food_library
for each row execute function public.set_food_library_updated_at();
