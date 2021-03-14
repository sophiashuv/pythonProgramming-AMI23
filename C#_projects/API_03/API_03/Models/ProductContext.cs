using System;
using Microsoft.EntityFrameworkCore;

namespace API_03.Models
{
    public class ProductContext : DbContext
    {
        public ProductContext(DbContextOptions<ProductContext> options)
            : base(options)
        {
        }

        public DbSet<ProductItem> ProductItems { get; set; }
    }
}
