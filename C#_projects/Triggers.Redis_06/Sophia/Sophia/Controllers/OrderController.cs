using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Sophia.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
using Sophia.Cache;

namespace Sophia.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class OrderController: ControllerBase
    {
        private readonly DatabaseContext _databaseContext;
        private readonly IRedisCache _cacheClient;

        public OrderController(DatabaseContext databaseContext, IRedisCache cacheClient)
        {
            _databaseContext = databaseContext;
            _cacheClient = cacheClient;
        }

        [HttpGet("{id?}")]
        public IEnumerable<Order> List(int? Id)
        {
            var userId = User.Claims
                .Where(c => c.Type == ClaimsIdentity.DefaultNameClaimType)
                .Select(c => c.Value)
                .SingleOrDefault();
            var userRole = User.Claims
                .Where(c => c.Type == ClaimsIdentity.DefaultRoleClaimType)
                .Select(c => c.Value)
                .SingleOrDefault();

            if (userRole == UserRole.Admin.ToString())
            {
                return _databaseContext.Orders.Include("Product");
            }

            if (Id.HasValue)
            {
                return _databaseContext.Orders
                    .Include("Product")
                    .Where(order => order.Id == Id && order.UserId == int.Parse(userId));
                
            }
            else
            {
                return _databaseContext.Orders
                    .Include("Product")
                    .Where(order => order.UserId == int.Parse(userId));
            }
        }

        [HttpPost]
        public IActionResult Create(Order orderDTO)
        {
            var product = _databaseContext.Products.Find(orderDTO.ProductId);
            if(product == null)
            {
                return NotFound(new { status = 404, message = "Product was not found" });
            }

            var productsInOrder = orderDTO.Count;
            var inStock = product.Quantity;

            //var inStock = _databaseContext.Products
            //    .Where(product => product.Id == orderDTO.ProductId)
            //    .Sum(product => product.Quantity);

            if (productsInOrder > inStock)
            {
                return BadRequest(new
                {
                    status = 400,
                    message = $"There are no {productsInOrder} {product.Title}." +
                    $"Only {inStock} {product.Title} are available"
                });
            }

            var userId = User.Claims
                .Where(c => c.Type == ClaimsIdentity.DefaultNameClaimType)
                .Select(c => c.Value)
                .SingleOrDefault();

            var order = new Order()
            {
                ProductId = orderDTO.ProductId,
                Count = orderDTO.Count,
                CreatedAt = DateTime.Now,
                UserId = int.Parse(userId)
            };
            
            _databaseContext.Add(order);

            //var product = _databaseContext.Products.Find(orderDTO.ProductId);
            product.Quantity -= orderDTO.Count;
            _databaseContext.Products.Update(product);

            _databaseContext.SaveChanges();
            
            _cacheClient.RemoveAllCache();

            return Ok(new { status = 200, message = "Order has been created", order = order });
        }

        [HttpDelete("{id}")]
        public IActionResult Delete(int Id)
        {
            var order = _databaseContext.Orders.Find(Id);

            _databaseContext.Remove(order);

            var product = _databaseContext.Products.Find(order.ProductId);
            product.Quantity += order.Count;
            _databaseContext.Products.Update(product);

            _databaseContext.SaveChanges();
            
            _cacheClient.RemoveAllCache();

            return Ok(new { status = 200, message = "Order has been deleted" });
        }
    }
}
