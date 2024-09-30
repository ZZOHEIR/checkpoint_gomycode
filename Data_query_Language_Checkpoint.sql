create database Data_query_language_checkpoint ;
create table Products (ProductID int primary key not null, ProductName varchar(50), ProductType varchar(50), Price float);
create table Customer (CustomerID int primary key not null, CustomerName varchar(50), Email varchar(50), Phone varchar (50));
create table Orders (OrderID int primary key not null, CustomerID int not null, OrderDate date);
create table OrderDetail (OrderDetailID int primary key not null, OrderID int not null, ProductID int not null, Quantity int);
create table ProductTypes (ProductTypeID int primary key not null, ProductTypeName varchar(50));

alter table Orders add constraint fk_orderscustomer_id foreign key (CustomerID) references Customer (CustomerID);
alter table OrderDetail add constraint fk_orderdetailorders_id foreign key (orderID) references Orders (OrderID);
alter table OrderDetail add constraint fk_orderdetailproduct_id foreign key (ProductID) references Products (ProductID);

insert into Products(ProductID , ProductName, ProductType, Price) values 
(1, 'Widget A', 'Widget', 10.00), (2, 'Widget B', 'Widget', 15.00), (3, 'Gadget X', 'Gadget', 20.00),
(4, 'Gadget Y', 'Gadget', 25.00), (5, 'Doohickey Z', 'Doohickey',30.00);
insert into Customer (CustomerID, CustomerName, Email, Phone) values 
(1, 'John Smith', 'john@example.com', '123-456-7890'),
(2, 'Jane Doe', 'jane.doe@example.com', '987-654-3210'),
(3, 'Alice Brown', 'alice.brown@example.com', '456-789-0123');
insert into Orders (OrderID, CustomerID, OrderDate) values 
(101, 1, '2024-05-01'),
(102, 2, '2024-05-02'),
(103, 3, '2024-05-01'),
(104, 3, '2024-05-02'),
(105, 3, '2024-05-03'),
(106, 3, '2024-05-04'),
(107, 3, '2024-05-05'),
(108, 2, '2024-05-01'),
(109, 3, '2024-05-02'),
(110, 2, '2024-05-03'),
(111, 3, '2024-05-06'),
(112, 3, '2024-05-07'),
(113, 3, '2024-05-08')

insert into OrderDetail (OrderDetailID, OrderID, ProductID, Quantity) values 
(1, 101, 1, 20),
(2, 101, 3, 10),
(3, 102, 2, 30),
(4, 102, 4, 20),
(5, 103, 5, 10),
(6, 104, 5, 40),
(7, 105, 4, 120),
(8, 106, 4, 100),
(9, 107, 3, 54),
(10, 108, 2, 80),
(11, 109, 1, 20),
(12, 110, 1, 70),
(14, 111, 1, 90),
(15, 112, 1, 10),
(16, 113, 1, 5),

insert into ProductTypes (ProductTypeID, ProductTypeName) values 
(1, 'Widget'),
(2, 'Gadget'),
(3, 'Doohickey');

select * from Products ;
select * from Customer;
select * from Orders;
select * from OrderDetail;
select * from ProductTypes ;
/*retrieve the names of the products that have been ordered by at least one customer,
along with the total quantity of each product ordered.*/

select P.ProductName, C.CustomerName, sum(OD.Quantity) as Total_Quantity
from Products P
join OrderDetail OD
on P.ProductID = OD.ProductID
join Orders O
on O.OrderID = OD.OrderID
join Customer C
on C.CustomerID = O.CustomerID
group by P.ProductID, P.ProductName, C.CustomerName
order by Total_Quantity

/*Retrieve the names of the customers who have placed an order on every day of the week,
along with the total number of orders placed by each customer.*/

select C.CustomerName, count(O.OrderID) as Count_order 
from Customer C
Join Orders O
On O.CustomerID = C.CustomerID
where O.OrderDate between '29-04-2024' and '05-05-2024'
group by C.CustomerName

/*Retrieve the names of the customers who have placed the most orders, 
along with the total number of orders placed by each customer. */
select TOP 1 C.CustomerName, count(O.OrderID) as Count_order 
from Customer C
Join Orders O
On O.CustomerID = C.CustomerID
group by C.CustomerName
Order by Count_order desc;
/*Retrieve the names of the products that have been ordered the most, 
along with the total quantity of each product ordered.*/

Select TOP 1 P.ProductID, P.ProductName, count(OD.OrderID) as total_count from Products P
Join OrderDetail OD
ON P.ProductID = OD.ProductID
group by P.ProductID, P.ProductName
Order by total_count desc

/*Retrieve the names of customers who have placed an order for at least one widget.*/
Select C.CustomerName, count(P.ProductName) as Product_name
From Customer C
Join Orders O
On O.CustomerID = C.CustomerID
Join OrderDetail OD
On OD.OrderID = O.OrderID
Join Products P
On P.ProductID = OD.ProductID
Join ProductTypes PT
On PT.ProductTypeName = P.ProductType
where PT.ProductTypeName = 'Widget'
group by C.CustomerName

/*Retrieve the names of the customers who have placed an order for at least one widget and at least one gadget, 
along with the total cost of the widgets and gadgets ordered by each customer.	*/

Select C.CustomerName, sum(P.Price * OD.Quantity) as Total_cost 
From Customer C
Join Orders O
On O.CustomerID = C.CustomerID
Join OrderDetail OD
On OD.OrderID = O.OrderID
Join Products P
On P.ProductID = OD.ProductID
Join ProductTypes PT
On PT.ProductTypeName = P.ProductType
where PT.ProductTypeName = 'Widget' or PT.ProductTypeName = 'Gadget'
Group by C.CustomerName

/*Retrieve the names of the customers who have placed an order for at least one gadget, 
along with the total cost of the gadgets ordered by each customer.*/

Select C.CustomerName, sum(P.Price * OD.Quantity) as Total_cost 
From Customer C
Join Orders O
On O.CustomerID = C.CustomerID
Join OrderDetail OD
On OD.OrderID = O.OrderID
Join Products P
On P.ProductID = OD.ProductID
Join ProductTypes PT
On PT.ProductTypeName = P.ProductType
where PT.ProductTypeName = 'Widget'
Group by C.CustomerName

/*Retrieve the names of the customers who have placed an order for at least one doohickey, 
along with the total cost of the doohickeys ordered by each customer.*/

Select C.CustomerName, sum(OD.Quantity) as Total_Quantity, P.price, (P.price * sum(OD.Quantity)) as Total_Cost
From Customer C
Join Orders O
On O.CustomerID = C.CustomerID
Join OrderDetail OD
On OD.OrderID = O.OrderID
Join Products P
On P.ProductID = OD.ProductID
where P.ProductID = 5
group by C.CustomerName, P.price

/*Retrieve the names of the customers who have placed an order every day of the week, 
along with the total number of orders placed by each customer.*/

SELECT CustomerID , COUNT(OrderID) AS total_orders
FROM Orders
WHERE CustomerID IN (SELECT CustomerID
                     FROM Orders
					 GROUP BY CustomerID, OrderDate
					 HAVING COUNT(DISTINCT OrderDate) = 7
					 )
GROUP BY CustomerID

/*Retrieve the total number of widgets and gadgets ordered by each customer, 
along with the total cost of the orders.*/

select CS.CustomerName, sum(Total_num_Product) as WIDGETS_GADGETS_COUNT, sum(Total_cost) as TOTAL_COST
from  Customer CS
join (Select C.CustomerName, count(PT.ProductTypeName) as Total_num_Product, sum(P.Price * OD.Quantity) as Total_cost
From Customer C
Join Orders O
On O.CustomerID = C.CustomerID
Join OrderDetail OD
On OD.OrderID = O.OrderID
Join Products P
On P.ProductID = OD.ProductID
Join ProductTypes PT
On PT.ProductTypeName = P.ProductType
where PT.ProductTypeID != 3
Group by C.CustomerName, PT.ProductTypeName) as query_wigets_gadgets
on CS.CustomerName = query_wigets_gadgets.CustomerName
Group By CS.CustomerName





