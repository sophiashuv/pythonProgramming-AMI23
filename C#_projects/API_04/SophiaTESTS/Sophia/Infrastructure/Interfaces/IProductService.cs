using Sophia.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Sophia.Infrastructure.Interfaces
{
    public interface IProductService
    {
        IEnumerable<Product> List(string searchString, string sortOrder,
            string sortType, int page, int pageSize);
        Product GetById(int id);
        void Create(Product product);
        void Update(Product product);
        void Remove(int id);
        int Count();
    }
}