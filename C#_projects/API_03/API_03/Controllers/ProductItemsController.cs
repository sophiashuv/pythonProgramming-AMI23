using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using API_03.Models;
using MySqlConnector;
using System.Data;

namespace API_03.Controllers
{

    [Route("api/[controller]")]
    [ApiController]
    public class ProductItemsController : ControllerBase
    {
        public AppDb Db { get; }

        public ProductItemsController(AppDb db)
        {
            Db = db;
        }

        private readonly ProductContext _context;


        // GET: api/ProductItems
        [HttpGet]
        public async Task<ActionResult<IEnumerable<ProductItem>>> GetProductItems([FromQuery] ProductParameters productParameters)
        {
            await Db.Connection.OpenAsync();
            var query = new ProductItemQuery(Db);
            var result = await query.GetAllProducts(productParameters);
          
            return new OkObjectResult(result);
        }

        // GET: api/ProductItems/5
        [HttpGet("{id}")]
        public async Task<ActionResult<ProductItem>> GetProductItem(int id)
        {
            await Db.Connection.OpenAsync();
            var query = new ProductItemQuery(Db);
            var result = await query.FindOneAsync(id);
            if (result is null)
                return new NotFoundResult();
            return new OkObjectResult(result);
        }

        // PUT: api/ProductItems/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutProductItem(int id, [FromBody] ProductItem body)
        {
            foreach (var prop in typeof(ProductItem).GetProperties())
            {
                if (prop.GetValue(body) is null)
                {
                    return new UnprocessableEntityObjectResult("Validation Error");
                }
            }

            await Db.Connection.OpenAsync();
            var query = new ProductItemQuery(Db);
            var result = await query.FindOneAsync(id);
            if (result is null)
                return new NotFoundResult();
            result.Title = body.Title;
            result.Price = body.Price;
            result.Image_url = body.Image_url;
            result.Created_at = body.Created_at;
            result.Updated_at = body.Updated_at;
            result.Description = body.Description;
            await result.UpdateAsync();
            return new OkObjectResult(result);
        }

        // POST: api/ProductItems
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<ProductItem>> PostProductItem([FromBody] ProductItem body)
        {

            foreach (var prop in typeof(ProductItem).GetProperties())
            {
                if (prop.GetValue(body) is null)
                {
                    return new UnprocessableEntityObjectResult("Validation Error");
                }
            }

            await Db.Connection.OpenAsync();
            body.Db = Db;
            
            await body.InsertAsync();
            return new OkObjectResult(body);
            
        }

        // DELETE: api/ProductItems/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteProductItem(int id)
        {
            await Db.Connection.OpenAsync();
            var query = new ProductItemQuery(Db);
            var result = await query.FindOneAsync(id);
            if (result is null)
                return new NotFoundResult();
            await result.DeleteAsync();
            return new OkResult();
        }

       
    }
}
