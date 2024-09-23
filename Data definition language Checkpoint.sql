Create database CHECK_POINT;

Create table Customers (
                        CustomerID int Primary Key,
						FirstName varchar (50),
						LastName varchar (50),
						Email varchar (50),
						Phone int,
						Address varchar(50),
						City varchar (50),
						State varchar (50),
						ZipCode int
						);
Create table Products (
                 ProductID int Primary Key,
				 ProductName varchar (50),
				 Description varchar (200),
				 Price decimal (8,2),
				 StockQuantity int,
				 	 );

create table Categories (
                         CategoryID int Primary Key,
				         CategoryName varchar (50),
				         Description varchar (50),
						 );

Create table Orders (
                      OrderID int Primary Key,
					  OrderDate date,
					  TotalAmount int
					  );
create table OrderDetails (
                            OrderDetailID int Primary Key,
							Quantity int,
							UnitPrice decimal (8,2),
							);
Alter table products ADD CategoryID int;
Alter table products ADD CONSTRAINT CategoryID FOREIGN KEY (CategoryID) references Categories (CategoryID);
Alter table orders ADD CustomerID int;
Alter table orders ADD CONSTRAINT CustomerID FOREIGN KEY (CustomerID) references Customers (CustomerID);
Alter table OrderDetails ADD OrderID int;
Alter table OrderDetails ADD CONSTRAINT OrderID FOREIGN KEY (OrderID)  references Orders (OrderID);
Alter table OrderDetails ADD ProductID int;
Alter table OrderDetails ADD CONSTRAINT ProductID FOREIGN KEY (ProductID) references Products (ProductID);

-- Ajout Not null apres creation des tables
--products
ALTER TABLE products ALTER COLUMN ProductName varchar(50) NOT NULL;
ALTER TABLE products ALTER COLUMN Description varchar (200) NOT NULL;
ALTER TABLE products ALTER COLUMN Price decimal (8,2) NOT NULL;
ALTER TABLE products ALTER COLUMN StockQuantity int NOT NULL;
--customers
ALTER TABLE Customers ALTER COLUMN CustomerID int NOT NULL;
ALTER TABLE Customers ALTER COLUMN FirstName varchar (50) NOT NULL;
ALTER TABLE Customers ALTER COLUMN LastName varchar (50) NOT NULL;
ALTER TABLE Customers ALTER COLUMN Email varchar (50) NOT NULL;
ALTER TABLE Customers ALTER COLUMN Phone int NOT NULL;
ALTER TABLE Customers ALTER COLUMN Address varchar(50) NOT NULL;
ALTER TABLE Customers ALTER COLUMN City varchar (50) NOT NULL;
ALTER TABLE Customers ALTER COLUMN State varchar (50) NOT NULL;
ALTER TABLE Customers ALTER COLUMN ZipCode int NOT NULL;
--Categories
ALTER TABLE Categories ALTER COLUMN CategoryID int NOT NULL;
ALTER TABLE Categories ALTER COLUMN CategoryName varchar (50) NOT NULL;
ALTER TABLE Categories ALTER COLUMN Description varchar (50) NOT NULL;
--orders
ALTER TABLE orders ALTER COLUMN OrderID int NOT NULL;
ALTER TABLE orders ALTER COLUMN OrderDate date NOT NULL;
ALTER TABLE orders ALTER COLUMN TotalAmount int NOT NULL;
--OrderDetails
ALTER TABLE OrderDetails ALTER COLUMN OrderDetailID int NOT NULL;
ALTER TABLE OrderDetails ALTER COLUMN Quantity int NOT NULL;
ALTER TABLE OrderDetails ALTER COLUMN UnitPrice decimal (8,2) NOT NULL;