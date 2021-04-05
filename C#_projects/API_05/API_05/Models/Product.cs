using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;
using static API_05.Models.Validation;

namespace API_05.Models
{
    public class Product
    {
        [Required]
        public int Id { get; set; }

        [Required]
        public string Description { get; set; }

        [Required]
        [Title]
        public string Title { get; set; }

        [Required]
        [ImageUrl]
        public string ImageUrl { get; set; }

        [Required]
        [Price]
        public double Price { get; set; }

        [Required]
        [Range(0, 1000)]
        public int Quantity { get; set; }

        [Required]
        public DateTime CreatedAt { get; set; }

        [Required]
        public DateTime UpdatedAt { get; set; }
    }
}