// Ganti dengan nomor WhatsApp Tentram yang sebenarnya.
export const WA_NUMBER = '6287790507560';

/** Build a wa.me deep link with an optional pre-filled message. */
export const wa = (msg?: string) =>
	msg
		? `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(msg)}`
		: `https://wa.me/${WA_NUMBER}`;