using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Sophia.Models
{
    public class ProductParams
    {
        public int Offset { get; set; }
        public int Limit { get; set; }
        public string Sort_by { get; set; } = "Title";
        public string Sort_type { get; set; } = "asc";
        public string Search { get; set; }
    }
}