using Microsoft.AspNetCore.Mvc;
using Sophia.Controllers;
using Sophia.Infrastructure.Interfaces;
using Sophia.Models;
using System;
using Xunit;

namespace Sophia.Test
{
    public class UnitTest
    {
        ProductController controller;
        IProductService service;

        public UnitTest()
        {
            service = new ProductsFakeData();
            controller = new ProductController(service);
        }

        [Fact]
        public void GetAllProducts_OK()
        {
            Assert.IsType<OkObjectResult>(controller.List("", "", "", 0, 0, null));
        }

        [Fact]
        public void GetProductById_OK()
        {
            Assert.IsType<OkObjectResult>(controller.List("", "", "", 0, 0, 1));
        }

        [Fact]
        public void GetProductById_Error404()
        {
            Assert.IsType<NotFoundObjectResult>(controller.List("", "", "", 0, 0, 100));
        }

        [Fact]
        public void CreateProduct_OK()
        {
            Product product = new Product
            {
                Id = 4,
                Title = "Banana",
                Description = "Banana description",
                ImageUrl = "banana.jpg",
                Price = 30,
                Quantity = 10,
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };
            Assert.IsType<OkObjectResult>(controller.Create(product));
        }

        [Fact]
        public void CreateProduct_Error400()
        {
            Product product = new Product
            {
                Id = 4,
                Title = "Banana",
                Description = "Banana description",
                ImageUrl = "banana.jpg",
                Price = 30,
                Quantity = 10,
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };
            controller.ModelState.AddModelError("ImageUrl",
                "Incorrect image_url.");
            var result = controller.Create(product);
            Assert.IsType<BadRequestObjectResult>(result);
        }

        [Fact]
        public void DeleteProduct_Ok()
        {
            var r = controller.Delete(1);
            Assert.IsType<OkObjectResult>(r);
        }

        [Fact]
        public void DeleteProduct_Error404()
        {
            var r = controller.Delete(100);
            Assert.IsType<NotFoundObjectResult>(r);
        }

        [Fact]
        public void EditProduct_Ok()
        {
            Product product = new Product
            {
                Id = 4,
                Title = "Banana",
                Description = "Banana description",
                ImageUrl = "banana.jpg",
                Price = 30,
                Quantity = 10,
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };
            var result = controller.Update(product);
            var t = service.GetById(product.Id);
            Assert.IsType<OkObjectResult>(result);
        }

        [Fact]
        public void EditProduct_Error400()
        {
            Product product = new Product
            {
                Id = 4,
                Title = "Banana 5",
                Description = "Banana description",
                ImageUrl = "banana.jpg",
                Price = 30,
                Quantity = 10,
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };
            controller.ModelState.AddModelError("Title",
                "Title must not contain integers.");
            var result = controller.Update(product);
            Assert.IsType<BadRequestObjectResult>(result);
        }
    }
}