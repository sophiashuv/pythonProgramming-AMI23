using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Sophia.Models
{
    public class LineItem
    {
        public int Id { get; set; }

        public int ProductId { get; set; }

        public long OrderedCount { get; set; }
    }
}