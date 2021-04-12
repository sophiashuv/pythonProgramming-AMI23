using Microsoft.AspNetCore.Mvc;
using Sophia.Infrastructure.Interfaces;
using Sophia.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Sophia.Controllers
{
    [Route("api/[controller]")]
    public class ProductController : ControllerBase
    {
        private readonly IProductService _productService;

        public ProductController(IProductService productService)
        {
            _productService = productService;
        }

        // GET: api/Product/5
        /// <summary>
        /// Returns a specific ProductItem or all products.
        /// </summary>
        /// <param name="id"></param>
        /// <response code="200">Gets an item</response>
        /// <response code="404">If the item is not found</response>
        [HttpGet("{id?}")]
        public IActionResult List(string searchString, string sortOrder,
            string sortType, int page, int pageSize, int? Id)
        {
            if (Id.HasValue)
            {
                var product = _productService.GetById(Id.Value);
                if (product == null) {
                    return NotFound(new { status = 404, massage = "Product is not found" });
                }
                return Ok(product);
            }
            var list = _productService.List(searchString, sortOrder,
                sortType, page, pageSize);
            return Ok ( new
            {
                products = list,
                count = _productService.Count()
            });
        }

        // POST: api/Product
        /// <summary>
        /// Creates a ProductItem.
        /// </summary>
        /// <remarks>
        /// Sample request:
        ///
        /// 
        ///     POST /ProductItem
        ///             {
        ///                   "description": "description",
        ///                   "title": "Product A",
        ///                   "image_url": "image.png",
        ///                   "price": 90.7,
        ///                   "created_at": "2019-11-17",
        ///                   "updated_at": "2019-11-18"
        ///              }
        ///
        /// </remarks>
        /// <param name="item"></param>
        /// <returns>A newly created ProductItem</returns>
        /// <response code="200">Returns the newly created item</response>
        /// <response code="400">If the item unvalid</response>
        [HttpPost]
        public IActionResult Create(Product model)
        {
            if (ModelState.IsValid)
            {
                _productService.Create(model);
                return Ok(new { status = 200, message = "Product has been created", product=model});
            }
            return BadRequest(ModelState);
        }


        // PUT: api/Product/5
        /// <summary>
        /// Edits a ProductItem.
        /// </summary>
        /// <remarks>
        /// Sample request:
        ///
        /// 
        ///     PUT /ProductItem
        ///             {
        ///                   "id": 0,
        ///                   "description": "description",
        ///                   "title": "Product A",
        ///                   "image_url": "image.png",
        ///                   "price": 90.7,
        ///                   "created_at": "2019-11-17",
        ///                   "updated_at": "2019-11-18"
        ///              }
        ///
        /// </remarks>
        /// <param name="item"></param>
        /// <returns>An edited ProductItem</returns>
        /// <response code="200">Returns the newly created item</response>
        /// <response code="400">If the item unvalid</response>
        [HttpPut]
        public IActionResult Update([FromBody] Product model)
        {
            if (ModelState.IsValid)
            {
                _productService.Update(model);
                return Ok(new { status = 200, message = "Product has been edited", produvt=model });
            }
            return BadRequest(ModelState);
        }

        // DELETE: api/Product/5
        /// <summary>
        /// Deletes a specific ProductItem.
        /// </summary>
        /// <param name="id"></param>
        /// <response code="200">Deletes item</response>
        /// <response code="404">If the item is not found</response>
        [HttpDelete("{id}")]
        public IActionResult Delete(int Id)
        {
            if (_productService.GetById(Id) == null)
            {
                return NotFound(new { status = 404, massage = "Product is not found" });
            }
            else
            {
                _productService.Remove(Id);
                return Ok(new { status = 200, message = "Product has been deleted" }); ;
            }
        }
    }
}