using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using API_05.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace API_05.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class ProductController : ControllerBase
    {
        private readonly DatabaseContext _databaseContext;

        public ProductController(DatabaseContext databaseContext)
        {
            _databaseContext = databaseContext;
        }

        [HttpGet("{id?}")]
        public IEnumerable<Product> List(int? Id)
        {
            if (Id.HasValue)
            {
                return _databaseContext.Products.Where(product => product.Id == Id);
            }
            else
            {
                return _databaseContext.Products;
            }
        }

        [HttpPost]
        [Route("/buy/{id}")]
        public void BuyProduct(int id)
        {
            List<Product> products = _databaseContext.Products.ToList();
            Product p = products.Find(p => p.Id == id);
            if (p != null)
            {
                p.Quantity -= 1;
                _databaseContext.SaveChanges();
            }
        }

        [HttpPost]
        [Authorize(Roles = "Admin")]
        public string Create(Product model)
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

            return product.Id.ToString();
        }

        [HttpPut("{id}")]
        [Authorize(Roles = "Admin")]
        public string Update(int id, [FromBody] Product model)
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

            return product.Id.ToString();
        }

        [HttpDelete("{id}")]
        [Authorize(Roles = "Admin")]
        public IActionResult Delete(int Id)
        {
            var product = new Product() { Id = Id };
            _databaseContext.Attach(product);
            _databaseContext.Remove(product);
            _databaseContext.SaveChanges();

            return Ok();
        }
    }
}
