export interface Situation {
	img: string;
	title: string;
	body: string;
	cta: string;
	msg: string;
}

export interface Reason {
	emoji: string;
	title: string;
	body: string;
}

export interface Step {
	n: string;
	title: string;
	body: string;
}

export interface Review {
	name: string;
	area: string;
	text: string;
}

export interface Faq {
	q: string;
	a: string;
}

export const situations: Situation[] = [
	{ img: '/standar-kami.png', title: 'Baru Renovasi', body: 'Dibuangi debu, sisa semen, dan bekas cat hingga siap ditempati.', cta: 'Saya baru renovasi', msg: 'Halo Tentram, saya baru selesai renovasi rumah dan butuh pembersihan. Boleh minta penawaran?' },
	{ img: '/airbnb-propertisewa.png', title: 'Baru Pindahan', body: 'Setiap sudut dibersihkan sebelum Anda mulai menempati.', cta: 'Saya baru pindahan', msg: 'Halo Tentram, saya baru pindah rumah dan ingin move in cleaning. Boleh minta penawaran?' },
	{ img: '/hero-v3.png', title: 'Rumah Terasa Kotor', body: 'Tidak sempat membersihkan sendiri? Biarkan kami membantu.', cta: 'Saya butuh home cleaning', msg: 'Halo Tentram, saya butuh home cleaning untuk rumah saya. Boleh minta penawaran?' },
	{ img: '/kantor.png', title: 'Office Cleaning', body: 'Lingkungan kerja yang lebih nyaman untuk tim dan pelanggan.', cta: 'Saya butuh office cleaning', msg: 'Halo Tentram, kantor kami butuh cleaning rutin/berkala. Boleh minta penawaran?' },
	{ img: '/deepcleantoilet.png', title: 'Deep Cleaning', body: 'Pembersihan menyeluruh hingga area yang jarang dibersihkan.', cta: 'Lihat deep cleaning', msg: 'Halo Tentram, saya tertarik dengan layanan Deep Cleaning. Boleh minta penawaran?' },
	{ img: '/HydroCleaning.png', title: 'Hydro Cleaning', body: 'Cuci sofa, kasur, dan karpet dengan teknologi hydro extraction.', cta: 'Lihat hydro cleaning', msg: 'Halo Tentram, saya tertarik dengan layanan Hydro Cleaning (cuci sofa/kasur/karpet). Boleh minta penawaran?' },
	{ img: '/cuci-ac.png', title: 'Cuci AC', body: 'AC dingin maksimal dan bebas bau tanpa perlu bongkar sendiri.', cta: 'Saya butuh cuci AC', msg: 'Halo Tentram, saya butuh layanan cuci AC. Boleh minta penawaran?' },
	{ img: '/gudang.png', title: 'Cleaning Gudang', body: 'Bersihkan debu dan kotoran menumpuk agar gudang rapi dan aman digunakan.', cta: 'Saya butuh cleaning gudang', msg: 'Halo Tentram, saya butuh layanan cleaning gudang. Boleh minta penawaran?' },
	{ img: '/kamar-mandi.png', title: 'Cleaning Kamar Mandi', body: 'Hilangkan kerak, jamur, dan bau tak sedap hingga kamar mandi kembali kinclong.', cta: 'Saya butuh cleaning kamar mandi', msg: 'Halo Tentram, saya butuh layanan cleaning kamar mandi. Boleh minta penawaran?' },
];

export const reasons: Reason[] = [
	{ emoji: '📅', title: 'Bisa Pilih Jadwal', body: 'Atur waktu cleaning sesuai jadwal Anda.' },
	{ emoji: '🧑‍🤝‍🧑', title: 'Bisa Pilih Mitra', body: 'Pilih mitra cleaning kepercayaan Anda.' },
	{ emoji: '🔄', title: 'Bisa Reschedule', body: 'Ubah jadwal dengan mudah tanpa ribet.' },
	{ emoji: '💳', title: 'Bisa Bayar Pakai Apa Aja', body: 'Berbagai metode pembayaran didukung.' },
];

export const steps: Step[] = [
	{ n: '1', title: 'Hubungi WhatsApp', body: 'Chat tim kami, fast response.' },
	{ n: '2', title: 'Ceritakan kebutuhan Anda', body: 'Jelaskan situasi rumah atau kantor.' },
	{ n: '3', title: 'Terima estimasi', body: 'Estimasi harga transparan.' },
	{ n: '4', title: 'Tim datang', body: 'Tim profesional datang sesuai jadwal.' },
	{ n: '5', title: 'Rumah kembali bersih', body: 'Nikmati hasilnya, siap digunakan.' },
];

export const reviews: Review[] = [
	{ name: 'Dewi A.', area: 'BSD', text: 'Baru pindah dan rumah langsung bersih maksimal. Timnya teliti banget.' },
	{ name: 'Reza P.', area: 'Jakarta Selatan', text: 'Setelah renovasi parah debunya. Tentram beresin sampai bersih, siap ditempati.' },
	{ name: 'Sinta M.', area: 'Gading Serpong', text: 'Pakai layanan rutin. Selalu tepat waktu dan hasilnya konsisten.' },
];

export const areas: string[] = [
	'Jakarta Selatan', 'Jakarta Barat', 'Jakarta Utara', 'Jakarta Timur', 'BSD City', 'Gading Serpong', 'Alam Sutera', 'Bintaro', 'Tangerang', 'Bekasi',
];

export const faqs: Faq[] = [
	{ q: 'Apakah tim membawa alat sendiri?', a: 'Ya. Tim Tentram datang dengan peralatan lengkap, Anda tidak perlu menyiapkan apa pun.' },
	{ q: 'Berapa lama proses cleaning?', a: 'Tergantung luas dan kondisi ruangan. Home cleaning biasanya 3–5 jam, deep cleaning bisa lebih lama. Estimasi pasti diberikan saat booking.' },
	{ q: 'Bagaimana menentukan harga?', a: 'Harga disesuaikan dengan luas area, jenis layanan, dan kondisi. Semua transparan, tanpa biaya tersembunyi.' },
	{ q: 'Apakah bisa datang di akhir pekan?', a: 'Bisa. Kami menyediakan jadwal fleksibel termasuk akhir pekan sesuai ketersediaan.' },
	{ q: 'Bagaimana jika saya tidak puas?', a: 'Setiap pekerjaan mengikuti quality checklist. Jika ada yang tidak sesuai, hubungi kami dan kami akan menindaklanjutinya.' },
];