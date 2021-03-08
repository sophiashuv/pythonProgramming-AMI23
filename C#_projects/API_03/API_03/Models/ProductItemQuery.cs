using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Common;
using System.Threading.Tasks;
using API_03.Controllers;
using MySqlConnector;

namespace API_03.Models
{
    public class ProductItemQuery
    {
        public AppDb Db { get; }

        public ProductItemQuery(AppDb db)
        {
            Db = db;
        }

        public async Task<ProductItem> FindOneAsync(int id)
        {
            using var cmd = Db.Connection.CreateCommand();
            cmd.CommandText = @"SELECT `id`, `_title`, `_price`, `_image_url`, `_created_at`, `_updated_at`, `description` FROM `product` WHERE `id` = @id";
            cmd.Parameters.Add(new MySqlParameter
            {
                ParameterName = "@id",
                DbType = DbType.Int32,
                Value = id,
            });
            var result = await ReadAllAsync(await cmd.ExecuteReaderAsync());
            return result.Count > 0 ? result[0] : null;
        }

        public async Task<List<ProductItem>> GetAllProducts(ProductParameters productParameters)
        {
            using var cmd = Db.Connection.CreateCommand();
            cmd.CommandText = @"SELECT * FROM product ";
            var search = productParameters.Search;
            var sort_type = productParameters.Sort_type;
            var sort_by = productParameters.Sort_by;
            var size = productParameters.PageSize;
            var offset = productParameters.Offset;
            if (search != null)
            {
                cmd.CommandText = cmd.CommandText +
                    "WHERE `_title` LIKE '%" + search + "%' OR `description` LIKE '%" + search + "%' OR `_created_at` LIKE '%" + search + "%' OR `_updated_at` LIKE '%" + search + "%' OR `_image_url` LIKE '%" + search + "%' OR `_price` LIKE '%" + search + "%' ";
            }
            if (sort_by != null)
            {
                cmd.CommandText = cmd.CommandText + " ORDER BY " + sort_by;
            }
       
            if (sort_type == "desc" || sort_type == "asc")
            {
                cmd.CommandText = cmd.CommandText + " " + sort_type;
            }
            if (size != 0)
            {
                cmd.CommandText = cmd.CommandText + " LIMIT " + size;
            }
            if (offset != 0)
            {
                cmd.CommandText = cmd.CommandText + " OFFSET " + offset;
            }
            cmd.CommandText = cmd.CommandText + ";";
            Console.WriteLine(cmd.CommandText);
            return await ReadAllAsync(await cmd.ExecuteReaderAsync());
        }


        public async Task DeleteAllAsync()
        {
            using var txn = await Db.Connection.BeginTransactionAsync();
            using var cmd = Db.Connection.CreateCommand();
            cmd.CommandText = @"DELETE FROM `product`";
            await cmd.ExecuteNonQueryAsync();
            await txn.CommitAsync();
        }

        private async Task<List<ProductItem>> ReadAllAsync(DbDataReader reader)
        {
            var posts = new List<ProductItem>();
            using (reader)
            {
                while (await reader.ReadAsync())
                {
                    var post = new ProductItem(Db)
                    {
                        Id = reader.GetInt32(0),
                        Title = reader.GetString(1),
                        Price = reader.GetDouble(2),
                        Image_url = reader.GetString(3),
                        Created_at = reader.GetString(4),
                        Updated_at = reader.GetString(5),
                        Description = reader.GetString(6)
                    };
                    posts.Add(post);
                }
            }
            return posts;
        }
    }
}
