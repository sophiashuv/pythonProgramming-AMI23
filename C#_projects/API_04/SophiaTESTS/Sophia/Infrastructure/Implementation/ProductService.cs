using Sophia.Infrastructure.Interfaces;
using Sophia.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Threading.Tasks;

namespace Sophia.Infrastructure.Implementation
{
    public class ProductService : IProductService
    {
        private readonly DatabaseContext _databaseContext;

        public ProductService(DatabaseContext databaseContext)
        {
            _databaseContext = databaseContext;
        }

        public IEnumerable<Product> List(string searchString, string sortOrder,
            string sortType, int page, int pageSize)
        {
            List<Product> products = Search(_databaseContext.Products.ToList(), searchString);
            products = Sort(products, sortOrder, sortType);

            if (page < 1 || page == 0) page = 1;
            if (pageSize < 1 || pageSize == 0) pageSize = products.Count();

            List<Product> pagedProducts = products
                .Skip((page - 1) * pageSize)
                .Take(pageSize).ToList();

            return pagedProducts;
        }

        private List<Product> Search(List<Product> products, string searchString)
        {
            List<Product> result = new List<Product>();
            if (!String.IsNullOrEmpty(searchString))
            {
                foreach (Product product in products)
                {
                    foreach (PropertyInfo item in typeof(Product).GetProperties())
                    {
                        if (product.GetType().GetProperty(item.Name).GetValue(product, null)
                            .ToString().ToLower().Contains(searchString.ToLower()) &&
                            !result.Contains(product))
                            result.Add(product);
                    }
                }
            }
            else
            {
                result = products;
            }
            return result;
        }

        private List<Product> Sort(List<Product> result, string sortOrder, string sortType)
        {
            foreach (var item in typeof(Product).GetProperties())
            {
                if (item.Name == sortOrder && sortType == "desc")
                {
                    result = result.OrderByDescending(c =>
                        c.GetType().GetProperty(sortOrder).GetValue(c, null))
                        .ToList();
                    return result;
                }
                else if (item.Name == sortOrder)
                {
                    result = result.OrderBy(c =>
                        c.GetType().GetProperty(sortOrder).GetValue(c, null))
                        .ToList();
                    return result;
                }
            }
            return result;
        }

        public Product GetById(int id)
        {
            return _databaseContext.Products.Find(id);
        }

        public void Create(Product productModel)
        {
            var product = new Product()
            {
                Description = productModel.Description,
                Title = productModel.Title,
                ImageUrl = productModel.ImageUrl,
                Price = productModel.Price,
                Quantity = productModel.Quantity,
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };

            _databaseContext.Add(product);
            _databaseContext.SaveChanges();
        }

        public void Update(Product productModel)
        {
            _databaseContext.Update(productModel);
            _databaseContext.SaveChanges();
        }

        public void Remove(int id)
        {
            var product = _databaseContext.Products.Find(id);
            _databaseContext.Remove(product);
            _databaseContext.SaveChanges();
        }

        public int Count()
        {
            return _databaseContext.Products.Count();
        }
    }
}