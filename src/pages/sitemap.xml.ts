import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export const GET: APIRoute = async ({ site }) => {
	const posts = (await getCollection('blog')).sort(
		(a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
	);

	const routes = [
		'/',
		'/blog/',
		'/register-pin/',
		'/reset-pin/',
	];

	const blogPostUrls = posts.map((post) => `/blog/${post.id}/`);
	const allUrls = [...routes, ...blogPostUrls];

	const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allUrls
		.map(
			(url) => `	<url>
		<loc>${new URL(url, site).toString()}</loc>
	</url>`
		)
		.join('\n')}
</urlset>`;

	return new Response(sitemap, {
		headers: {
			'Content-Type': 'application/xml',
		},
	});
};
