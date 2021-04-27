using Microsoft.EntityFrameworkCore;
using API_05.Authentication;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace API_05.Models
{
    public class DatabaseContext : DbContext
    {
        public DatabaseContext(DbContextOptions<DatabaseContext> options)
            : base(options) { }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            var hasher = new CustomPasswordHasher(1000);
            modelBuilder.Entity<Identity>().HasData(
                new Identity
                {
                    Id = 1,
                    Email = "admin@gmail.com",
                    Password = hasher.Hash("admin"),
                    FirstName = "admin",
                    LastName = "admin",
                    Role = UserRole.Admin
                }
            );
        }

        public DbSet<Identity> Identities { get; set; }
        public DbSet<Product> Products { get; set; }
    }
}