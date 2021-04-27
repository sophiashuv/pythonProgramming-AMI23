using Sophia.Infrastructure.Interfaces;
using Sophia.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Sophia.Test
{
    class ProductsFakeData : IProductService
    {
        private readonly List<Product> products;

        public ProductsFakeData()
        {
            products = new List<Product>()
            {
                new Product
                {
                    Id = 1,
                    Title = "Orange",
                    Description = "Orange description",
                    ImageUrl = "orange.jpg",
                    Price = 40,
                    Quantity = 50,
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                },
                new Product
                {
                    Id = 2,
                    Title = "Apple",
                    Description = "Apple description",
                    ImageUrl = "Apple.jpg",
                    Price = 10,
                    Quantity = 150,
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                },
                new Product
                {
                    Id = 3,
                    Title = "Tomato",
                    Description = "Tomato description",
                    ImageUrl = "tomato.jpg",
                    Price = 50,
                    Quantity = 20,
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow
                }
            };
        }

        public IEnumerable<Product> List(string searchString, string sortOrder,
            string sortType, int page, int pageSize)
        {
            return products;
        }

        public Product GetById(int id)
        {
            return products.Find(p => p.Id == id);
        }

        public void Create(Product newItem)
        {
            products.Add(newItem);
        }

        public void Remove(int id)
        {
            products.Remove(products.FirstOrDefault(c => c.Id == id));
        }

        public void Update(Product product)
        {
            products.Remove(products.Find(p => p.Id == product.Id));
            products.Add(product);
        }

        public int Count()
        {
            return products.Count();
        }
    }
}