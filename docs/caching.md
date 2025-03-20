# Caching Strategy

## Standalone Models
Standalone models have:
- `SINGLE_ITEM_CACHE_KEY`

## One-to-Many Relation Models
One-to-many relation models have:
- `SINGLE_ITEM_CACHE_KEY`
- `SINGLE_ITEMS_CACHE_KEY`

## Project Models and Cache Keys

The models in the project and their corresponding cache strategies:

### UserModel
- **Cache Strategy:**
    - `UserCache` → Caches a single user.

### LoggerModel (One-to-Many with ObtainedDataModel)
- **Cache Strategy:**
    - `SINGLE_ITEM_CACHE_KEY` → Caches a single logger by `logger_id`.
    - `SINGLE_ITEMS_CACHE_KEY` → Caches multiple loggers by `user_id`.

### ObtainedDataModel (Belongs to LoggerModel)
- **Cache Strategy:**
    - `SINGLE_ITEMS_CACHE_KEY` → Caches multiple `ObtainedDataModel` entries by `logger_id` (since `ObtainedDataModel` does not have an ID).

