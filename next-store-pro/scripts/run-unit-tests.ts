import { getProducts, getProductBySlug } from '@/lib/data';
import assert from 'assert';

// This is a manual test runner to work around the broken npm environment.
// It will perform real file system reads.

async function test_getProducts_fetches_all_products() {
  console.log('Running: test_getProducts_fetches_all_products...');
  const products = await getProducts();
  assert(Array.isArray(products), 'getProducts should return an array.');
  // We know from our sync script that there should be 5 products.
  assert.strictEqual(products.length, 5, 'getProducts should return 5 products.');
  console.log('  ✅ Passed');
}

async function test_getProductBySlug_returns_correct_product() {
  console.log('Running: test_getProductBySlug_returns_correct_product...');
  const slug = 'pro-notion-template-pack'; // A known slug from products.json
  const product = await getProductBySlug(slug);
  assert(product !== null, `Product with slug "${slug}" should be found.`);
  assert.strictEqual(product?.slug, slug, 'Product slug should match the requested slug.');
  console.log('  ✅ Passed');
}

async function test_getProductBySlug_returns_null_for_unknown_slug() {
  console.log('Running: test_getProductBySlug_returns_null_for_unknown_slug...');
  const slug = 'this-slug-does-not-exist';
  const product = await getProductBySlug(slug);
  assert.strictEqual(product, null, `Product with slug "${slug}" should not be found.`);
  console.log('  ✅ Passed');
}

async function runTests() {
  console.log('--- Running Unit Tests Manually ---');
  const tests = [
    test_getProducts_fetches_all_products,
    test_getProductBySlug_returns_correct_product,
    test_getProductBySlug_returns_null_for_unknown_slug,
  ];

  let failedCount = 0;

  for (const test of tests) {
    try {
      await test();
    } catch (error) {
      failedCount++;
      console.error(`  ❌ Failed: ${test.name}`);
      console.error(error);
    }
  }

  console.log('\n--- Test Run Complete ---');
  if (failedCount > 0) {
    console.error(`\n❌ ${failedCount} out of ${tests.length} tests failed.`);
    process.exit(1);
  } else {
    console.log(`\n✅ All ${tests.length} tests passed successfully.`);
  }
}

runTests();
