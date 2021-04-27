using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Sophia.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using Sophia.Cache;

namespace Sophia.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class ProductController : ControllerBase
    {
        private readonly DatabaseContext _databaseContext;
        private readonly IRedisCache _cacheClient;

        public ProductController(DatabaseContext databaseContext, IRedisCache cacheClient)
        {
            _databaseContext = databaseContext;
            _cacheClient = cacheClient;
        }

        [HttpGet("{id?}")]
        public IActionResult List(string searchString, string sortOrder,
            string sortType, int offset, int limit, int? Id)
        {
            if (Id.HasValue)
            {
                return Ok(_databaseContext.Products.Where(product => product.Id == Id));
            }
            else
            {
                List<Product> pagedProducts = _cacheClient.GetProducts(searchString, sortOrder, sortType, offset, limit);

                if (pagedProducts is null)
                {
                    List<Product> products = Search(_databaseContext.Products.ToList(), searchString);
                    products = Sort(products, sortOrder, sortType);

                    if (offset < 1 || offset == 0) offset = 1;
                    if (limit < 1 || limit == 0) limit = products.Count();

                    pagedProducts = products
                        .Skip((offset - 1) * limit)
                        .Take(limit).ToList();
                    
                    _cacheClient.SetProducts(searchString, sortOrder, sortType, offset, limit, pagedProducts);
                }
                
                return Ok(new { products = pagedProducts, count = _databaseContext.Products.Count() });
            }
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


        [HttpPost]
        [Authorize(Roles = "Admin")]
        public IActionResult Create(Product model)
        {
            var product = new Product()
            {
                Description = model.Description,
                Title = model.Title,
                ImageUrl = model.ImageUrl,
                Price = model.Price,
                Quantity = model.Quantity,
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };

            _databaseContext.Add(product);
            _databaseContext.SaveChanges();
            
            _cacheClient.RemoveAllCache();

            return Ok(new { status = 200, message = "Product has been created" });
        }

        [HttpPut("{id}")]
        [Authorize(Roles = "Admin")]
        public IActionResult Update(int id, [FromBody] Product model)
        {
            var product = new Product()
            {
                Id = id,
                Description = model.Description,
                Title = model.Title,
                ImageUrl = model.ImageUrl,
                Price = model.Price,
                Quantity = model.Quantity,
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };

            _databaseContext.Update(product);
            _databaseContext.SaveChanges();
            
            _cacheClient.RemoveAllCache();

            return Ok(new { status = 200, message = "Product has been edited" });
        }

        [HttpDelete("{id}")]
        [Authorize(Roles = "Admin")]
        public IActionResult Delete(int Id)
        {
            var product = _databaseContext.Products.Find(Id);
            //var product = new Product() { Id = Id };
            //_databaseContext.Attach(product);
            _databaseContext.Remove(product);
            _databaseContext.SaveChanges();
            
            _cacheClient.RemoveAllCache();

            return Ok(new { status = 200, message = "Product has been deleted" }); ;
        }
    }
}