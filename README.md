## Our Data Base structure
### Rol Table
| Field | Data Type |
|-------|-----------|
| ID    | (Primary Key) |
| name  |  |

### User Table
| Field    | Data Type    |
|----------|--------------|
| ID       | (Primary Key) |
| role_id  | (Foreign Key) |
| FirstName|              |
| LastName |              |

### Productos Table
| Field               | Data Type    |
|---------------------|--------------|
| ID                  | (Primary Key) |
| Name                |              |
| Price               |              |
| unit_compensation   |              |
| package_compensation|              |

### Production Table
| Field     | Data Type    |
|-----------|--------------|
| ID        | (Primary Key) |
| user_id   | (Foreign Key) |
| product_id| (Foreign Key) |
| amount    |              |
| date      |              |

## Our API structure