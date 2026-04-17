from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "postgresql://mahasiswa-rsi:praktikum-rsi@localhost:5433/acara-rsi"

# Create engine untuk SQLModel
engine = create_engine(DATABASE_URL, echo=False)  # echo=True untuk debug query

# Dependency session untuk router/service
def get_session():
    with Session(engine) as session:  # pakai sqlmodel.Session
        yield session

# Fungsi buat bikin semua tabel (dipanggil sekali)
def init_db():
    from src.database.schema.schema import User
    # dari sini nanti bisa ditambah model lain misal Role, Account, dll
    SQLModel.metadata.create_all(engine)